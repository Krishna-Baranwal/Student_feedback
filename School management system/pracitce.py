subjects = [
    "📐 Maths",
    "🔬 Science",
    "📖 English",
    "🌏 Social Science",
    "🧪 Chemistry",
    "🧮 Physics",
    "💻 Computer",
    "📘 Hindi",
    "🌱 Biology",
    "📊 Economics",
    "📚 Sanskrit",
    "🎨 Drawing",
    "🎵 Music",
    "🏋️ PT / Sports"
]
terms = [
    "📝 Unit Test 1",
    "🧪 Mid Term",
    "📊 Unit Test 2",
    "📓 Final Exam",
    "📆 Annual"
]
classes = [f"📚 Class {i}" for i in range(1, 13)]
def get_feedback(marks):
    if marks >= 90:
        return "🌟 Excellent!"
    elif marks >= 75:
        return "👍 Good Job!"
    elif marks >= 50:
        return "🙂 Keep Improving"
    else:
        return "⚠️ Need More Practice"




import streamlit as st
import requests
from time import sleep

API_URL = "http://127.0.0.1:8000"

st.title("🧠 Faculty - Zone")
teacher_name = st.sidebar.text_input("👨‍🏫 Name").title().strip()
password = st.sidebar.text_input("🔐 Password", type="password")

if "student_index" not in st.session_state:
    st.session_state.student_index = 0



if teacher_name and password:
    response_teacher_login = requests.get(f"{API_URL}/check/{teacher_name}/{password}")
    result = response_teacher_login.json()

    if result.get("status") == "success":
        st.sidebar.success(f"Welcome {teacher_name} 🎉")
        sleep(1)
        selected_class = st.sidebar.selectbox('📚 Select Class', [i for i in range(1, 9)])

        if selected_class:
            st.header("📘 Marks Entry Panel")
            response_marks_entry = requests.get(f"{API_URL}/show_students_for_result/{selected_class}")
            data = response_marks_entry.json()

            if "students" in data:
                students = data["students"]

                if st.session_state.student_index < len(students):
                    student = students[st.session_state.student_index]
                    name = student["name"]
                    roll = student["roll_num"]

                    st.markdown(f"### 👤 {name} (Roll: {roll})")
                    marks = {}
                    subjects = ["Maths", "Science", "English", "Hindi", "SST",
                                "Computer", "EVS", "General Knowledge", "Art", "Moral Science"]

                    for sub in subjects:
                        col1, col2 = st.columns(2)
                        with col1:
                            ext = st.number_input(f"{sub} External", 0, 80, key=f"{name}_{sub}_ext")
                        with col2:
                            internal = st.number_input(f"{sub} Internal", 0, 20, key=f"{name}_{sub}_int")
                        marks[sub] = {"external": ext, "internal": internal}

                    if st.button("✅ Submit Result"):
                        payload = {
                            "student_name": name,
                            "roll_num": roll,
                            "class_name": selected_class,
                            "teacher_name": teacher_name,
                            "marks": marks
                        }

                        res = requests.post(f"{API_URL}/add_result", json=payload)
                        if res.status_code == 200:
                            st.success(f"{name}'s marks submitted successfully!")
                            st.session_state.student_index += 1
                            st.rerun()

                        else:

                            st.error("❌ Submission failed. Try again.")
                else:
                    st.success("🎉 All students completed for this class!")
                    sleep(2)

                    st.header("📸 Verification Required")
                    st.info("Please capture your photo for authentication & transparency.")

                    image = st.camera_input("Take a photo")

                    if image:
                        from PIL import Image
                        import os


                        img = Image.open(image)

                        folder = "teacher_photos"
                        os.makedirs(folder, exist_ok=True)

                        file_path = f"{folder}/{teacher_name.replace(' ', '_')}.jpg"
                        img.save(file_path)

                        st.success("✅ Photo captured and saved successfully!")
                        st.balloons()

else:
        st.sidebar.error("❌ Incorrect Name or Password")



