import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.title("📋 Student Feedback Collector")
st.subheader("🧑‍🎓 Give Feedback to Your Teacher")
st.write("💡 Your feedback helps teachers improve and grow!")

tab1, tab2 = st.tabs(["📝 Fill Form", "📊 Analysis"])
with tab1:
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
                    st.info("Fill all details")
