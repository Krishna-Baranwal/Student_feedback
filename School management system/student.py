import streamlit as st
import pandas as pd
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="🎓 Student Panel", page_icon="📚")
tab1 , tab2 = st.tabs(["Result","Request to Principle"])
with tab1:
    st.title("🎓 Student Dashboard Panel")
    st.sidebar.subheader("🔐 Student Login")

    student_name = st.sidebar.text_input("🧑‍🎓 Student Name").strip().title()
    student_password = st.sidebar.text_input("🔑 Password", type="password").strip()

    if student_name and student_password:
        url = f"{API_URL}/verify_student/{student_name}/{student_password}"
        try:
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()

                if data.get("status") == "success":
                    name = data["name"]
                    class_id = data["class_id"]
                    roll_num = data["roll_num"]


                    st.sidebar.success("✅ Login successful!")
                    st.success(f"""
                    👋 Welcome, **{name}**  
                    🏫 Class: **{class_id}**  
                    🎫 Roll No: **{roll_num}**
                    """)

                    if st.button("📄 Show My Result"):
                        result_url = f"{API_URL}/show_result/{class_id}"
                        result_response = requests.get(result_url)

                        if result_response.status_code == 200:
                            df = pd.DataFrame(result_response.json().get("result", []))
                            df.columns = [col.lower().strip() for col in df.columns]

                            if "roll_num" in df.columns:
                                student_data = df[df["roll_num"] == roll_num]

                                if not student_data.empty:

                                    if "remaining_fees" in student_data.columns:
                                        pending_fees = int(student_data["remaining_fees"].values[0])
                                    else:
                                        pending_fees = 0


                                    if pending_fees > 0:
                                        st.error(f"💰 Please clear your pending fees (₹{pending_fees}) to view the result.")
                                    else:
                                        st.subheader("📊 Your Performance Summary")

                                        try:
                                            st.metric("📋 Total Marks", int(student_data["total"].values[0]))
                                            st.metric("🎯 Percentage", f"{round(student_data['percentage'].values[0], 2)}%")
                                            st.metric("🏁 Result", student_data["result_status"].values[0])
                                        except KeyError:
                                            st.warning("⚠️ Some result fields are missing.")

                                        column_map = {
                                            "maths_ext": "Maths (Ext)",
                                            "maths_int": "Maths (Int)",
                                            "science_ext": "Science (Ext)",
                                            "science_int": "Science (Int)",
                                            "english_ext": "English (Ext)",
                                            "english_int": "English (Int)",
                                            "english_grammar_ext": "Eng Grammar (Ext)",
                                            "english_grammar_int": "Eng Grammar (Int)",
                                            "hindi_ext": "Hindi (Ext)",
                                            "hindi_int": "Hindi (Int)",
                                            "hindi_grammar_ext": "Hindi Grammar (Ext)",
                                            "hindi_grammar_int": "Hindi Grammar (Int)",
                                            "social_science_ext": "Social Sci (Ext)",
                                            "social_science_int": "Social Sci (Int)",
                                            "arts_ext": "Arts (Ext)",
                                            "arts_int": "Arts (Int)",
                                            "computer_ext": "Computer (Ext)",
                                            "computer_int": "Computer (Int)"
                                        }

                                        ignore_columns = [
                                            "total", "percentage", "result_status",
                                            "fees", "fees_paid", "remaining_fees", "student_name",
                                            "roll_num", "student_class", "teacher_name"
                                        ]

                                        subject_data = student_data.drop(
                                            columns=[col for col in ignore_columns if col in student_data.columns],
                                            errors='ignore'
                                        ).T.reset_index()
                                        subject_data.columns = ["Subject Code", "Marks"]
                                        subject_data["Subject"] = subject_data["Subject Code"].map(column_map)
                                        subject_data.drop("Subject Code", axis=1, inplace=True)

                                        st.table(subject_data.set_index("Subject"))

                                else:
                                    st.warning("📲 Your result is not available yet. Please contact your teacher.")
                            else:
                                st.warning("⚠️ No result data found for this class.")
                        else:
                                st.error("🚫 Failed to fetch result data from server.")

                else:
                            st.sidebar.error("🚫 Server error! Please try again later.")

        except requests.exceptions.RequestException as e:
                st.sidebar.error(f"⚠️ Request Failed: {e}")
    else:
        st.sidebar.info("👈 Please enter your credentials to log in.")


if student_name and student_password:
    with tab2:
     st.title("📋 Student Feedback Collector")
     st.subheader("🧑‍🎓 Give Feedback to Your Teacher")
     st.write("💡 Your feedback helps teachers improve and grow!")
     with st.form("Fill the form"):
        st.markdown("🙏 **Please fill the form honestly**")

        name = st.text_input("🧒 Enter your name").title().strip()
        Class = st.selectbox("🏫 Enter your class", list(range(1, 13)))

        response = requests.get(f"{API_URL}/show")
        if response.status_code == 200:
            data = response.json()
            teacher_options = [f"{t['teacher_name']} - {t['subject']}" for t in data][1:]
        else:
            teacher_options = ["⚠️ No teacher data found"]

        selected_teacher = st.selectbox("👨‍🏫 Select Teacher & Subject", teacher_options)
        comment = st.text_area("💬 Enter your feedback").title()
        rating = st.number_input("⭐ Enter your rating", min_value=0.50, max_value=5.0, step=0.25, value=3.0)

        submitted = st.form_submit_button("📨 Submit Feedback")

        if submitted:
            if name and Class and selected_teacher and comment and rating:
                teacher_name, teacher_subject = selected_teacher.split(" - ")

                payload = {
                    "name": name,
                    "standard": Class,
                    "teacher_name": teacher_name,
                    "teacher_subject": teacher_subject,
                    "comment": comment,
                    "rating": rating
                }

                response_post = requests.post(f'{API_URL}/submit_form', json=payload)

                if response_post.status_code == 200:
                    st.success("✅ Feedback submitted successfully! Thank you 🙏")
                    st.balloons()
                else:
                    st.error("❌ Something went wrong! Please try again 🔄")

            else:
                st.error("Please fill all details")




