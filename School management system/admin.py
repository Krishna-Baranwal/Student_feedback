import streamlit as st
import requests
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Admin Panel", layout="wide")

st.title("🔐 Admin Control Panel 👨‍💼🎛️")
st.sidebar.subheader("🔐 Admin Login")

API_URL = "http://127.0.0.1:8000"

name = "Shri Harivansh"
password_ask = "2hit"
admin_name = st.sidebar.text_input("👨‍🏫 Name").title().strip()
password = st.sidebar.text_input("🔐 Password", type="password").strip()

if admin_name and password:
    if admin_name == name and password == password_ask:
       st.sidebar.success(f"✅ Welcome {admin_name} 👨‍💼 | Autonomy: Admin")
    else:
        st.sidebar.error("❌ Invalid admin credentials.")


    tab1, tab2 = st.tabs(["📊 Result Analysis", "➕ Add/Update"])

    with tab1:
        selected_class = st.sidebar.selectbox("📚 Select Class to View Result", list(range(1, 13)))
        if st.sidebar.button("🔍 Show Result"):
            response = requests.get(f"{API_URL}/select_class/{selected_class}")
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "success" and data.get("students"):
                    df = pd.DataFrame(data["students"])

                    if df.empty:
                        st.warning("⚠️ No result data available for this class.")
                    else:
                        st.dataframe(df, use_container_width=True)

                        if 'percentage' in df.columns:
                            pass_count = df[df['percentage'] >= 33].shape[0]
                            fail_count = df[df['percentage'] < 33].shape[0]

                            pie_data = pd.DataFrame({
                                'Result': ['✅ Pass', '❌ Fail'],
                                'Count': [pass_count, fail_count]
                            })
                            fig = px.pie(pie_data, names='Result', values='Count', title='📊 Pass vs Fail')
                            st.plotly_chart(fig)

                            subject_cols = ['maths_ext', 'science_ext', 'english_ext', 'hindi_ext']
                            avg_scores = df[subject_cols].mean().reset_index()
                            avg_scores.columns = ['📚 Subject', '📈 Average Marks']

                            fig = px.bar(avg_scores, x='📚 Subject', y='📈 Average Marks',
                                         title='📚 Subject-Wise Performance')
                            st.plotly_chart(fig)

                            st.metric("🎯 Average Percentage", round(df['percentage'].mean(), 2))
                            st.metric("✅ Total Passed", pass_count)
                            st.metric("❌ Total Failed", fail_count)
                        else:
                            st.warning("⚠️ 'percentage' column not found in result data.")
                else:
                    st.warning("⚠️ No student results found for this class.")
            else:
                st.error("🚫 Failed to fetch data from server.")

    with tab2:
        st.header("🔧 Admin Functional Features")
        st.write("🛠️ Select Operation")
        select_option = st.selectbox("Select Action", [
            "➕ Add Student", "🗑️ Delete Student", "👀 View Student", "🔁 Update Student",
            "➕ Add Teacher", "🗑️ Delete Teacher", "👀 View Teacher"
        ])

        if select_option == "➕ Add Student":
            st.subheader("🆕 Add New Student")
            with st.form("add_student_form", clear_on_submit=True):
                student_name = st.text_input("🧑‍🎓 Name")
                roll_num = st.number_input("🎫 Roll Number", min_value=1, step=1)
                class_id = st.selectbox("🏫 Class", list(range(1, 13)))
                fees = st.number_input("💰 Total Fees", min_value=0, step=100)
                fees_paid = st.number_input("💸 Fees Paid", min_value=0, step=100)
                email = st.text_input("📧 Email")
                password = st.text_input("🔑 Password", type="password")
                submitted = st.form_submit_button("✅ Add Student")

                if submitted:
                    if fees_paid > fees:
                        st.warning("❗ Fees paid cannot be greater than total fees.")
                    elif not all([student_name, roll_num, class_id, email, password]):
                        st.warning("⚠️ Please fill all the required fields.")
                    else:
                        student_data = {
                            "name": student_name,
                            "roll_num": roll_num,
                            "class_id": class_id,
                            "fees": fees,
                            "fees_paid": fees_paid,
                            "email": email,
                            "password": password
                        }
                        response = requests.post(f"{API_URL}/add_student", json=student_data)
                        if response.status_code == 200:
                            st.success("✅ Student added successfully!")
                        else:
                            st.error("🚫 Failed to add student.")

        elif select_option == "🗑️ Delete Student":
            st.subheader("🗑️ Delete Student Record")
            student_name_del = st.text_input("🧑‍🎓 Name")
            roll_num_del = st.number_input("🎫 Roll Number", min_value=1, step=1)
            class_id_del = st.selectbox("🏫 Class", list(range(1, 13)))
            if st.button("❌ Delete"):
                student_delete = {
                    'name': student_name_del,
                    'class_id': class_id_del,
                    'roll_num': roll_num_del
                }
                response_del = requests.post(f"{API_URL}/delete_student", json=student_delete)
                if response_del.status_code == 200:
                    st.success("✅ Student deleted successfully!")
                else:
                    st.error("🚫 Failed to delete student.")


        elif select_option == "👀 View Student":
            st.subheader("👀 View Student Info")
            student_name_show = st.text_input("🧑‍🎓 Name")
            roll_num_show = st.number_input("🎫 Roll Number", min_value=1, step=1)
            class_id_show = st.selectbox("🏫 Class", list(range(1, 13)))
            if st.button("🔍 Fetch Student"):
                try:
                    response_show = requests.get(
                        f"{API_URL}/show_student?name={student_name_show}&roll_num={roll_num_show}&class_id={class_id_show}"
                    )
                    if response_show.status_code == 200:
                        student_data = response_show.json()
                        student_info = student_data.get("result", {})
                        if student_info:
                            st.markdown("### 🧾 Basic Details")
                            basic_info = {
                                "Name": student_info.get("name"),
                                "Roll Number": student_info.get("roll_num"),
                                "Class": student_info.get("class_id"),
                                "Email": student_info.get("email"),
                                "Fees": student_info.get("fees"),
                                "Fees Paid": student_info.get("fees_paid")
                            }
                            st.table(pd.DataFrame(basic_info.items(), columns=["Field", "Value"]))
                            st.markdown("### 📊 Subject-wise Marks")
                            marks_data = student_info.get("marks", {})
                            if marks_data:
                                marks_df = pd.DataFrame.from_dict(marks_data, orient="index")
                                marks_df.index.name = "Subject"
                                st.dataframe(marks_df)
                            else:
                                st.info("📭 No marks found for this student.")
                        else:
                            st.warning("❗ No student data found.")
                    else:
                        st.error("🚫 Failed to fetch student.")
                except Exception as e:
                    st.error(f"❌ Error occurred: {e}")

        elif select_option == "🔁 Update Student":
            st.subheader("🔁 Update Student Email & Password")
            with st.form("update_form"):
                student_name_upd = st.text_input("🧑‍🎓 Name")
                roll_num_upd = st.number_input("🎫 Roll Number", min_value=1, step=1)
                class_id_upd = st.selectbox("🏫 Class", list(range(1, 13)))
                email_upd = st.text_input("📧 New Email")
                password_upd = st.text_input("🔑 New Password", type="password")
                submitted_upd = st.form_submit_button("✅ Update")

                if submitted_upd:
                    update_data = {
                        "name": student_name_upd,
                        "roll_num": roll_num_upd,
                        "class_id": class_id_upd,
                        "email": email_upd,
                        "password": password_upd
                    }
                    response = requests.post(f"{API_URL}/update_student", json=update_data)
                    if response.status_code == 200:
                        st.success("✅ Student updated successfully!")
                    else:
                        st.error("🚫 Failed to update student.")

        elif select_option == "➕ Add Teacher":
            st.subheader("➕ Add New Teacher")
            with st.form("add_teacher_form", clear_on_submit=True):
                teacher_name = st.text_input("👨‍🏫 Name")
                teacher_email = st.text_input("📧 Email")
                teacher_password = st.text_input("🔑 Password", type="password")
                teacher_class = st.selectbox("🏫 Class", list(range(1, 13)))
                submitted = st.form_submit_button("✅ Add Teacher")

                if submitted:
                    teacher_data = {
                        "name": teacher_name,
                        "email": teacher_email,
                        "password": teacher_password,
                        "teacher_class": teacher_class
                    }
                    response = requests.post(f"{API_URL}/add_teacher", json=teacher_data)
                    if response.status_code == 200:
                        st.success("✅ Teacher added successfully!")
                    else:
                        st.error("🚫 Failed to add teacher.")

        elif select_option == "🗑️ Delete Teacher":
            st.subheader("🗑️ Delete Teacher")
            teacher_name = st.text_input("👨‍🏫 Name")
            teacher_class = st.selectbox("🏫 Class", list(range(1, 13)))
            if st.button("❌ Delete Teacher"):
                response = requests.post(f"{API_URL}/delete_teacher", json={"name": teacher_name, "teacher_class": teacher_class})
                if response.status_code == 200:
                    st.success("✅ Teacher deleted successfully!")
                else:
                    st.error("🚫 Failed to delete teacher.")

        elif select_option == "👀 View Teacher":
            st.subheader("👀 View Teacher Info")
            if st.button("📄 Show All Teachers"):
                response = requests.get(f"{API_URL}/show_teachers")
                if response.status_code == 200:
                    data = response.json()
                    st.dataframe(pd.DataFrame(data["teachers"]), use_container_width=True)
                else:
                    st.error("🚫 Failed to fetch teachers.")
else:
    st.sidebar.info("👈 Please enter your credentials to log in.")
