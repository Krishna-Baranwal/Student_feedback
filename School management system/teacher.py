import streamlit as st
import requests
from datetime import datetime
import os
import logging
import pandas as pd
from time import sleep

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Teacher Panel", layout="wide")
logging.basicConfig(
    filename="login.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

tab1, tab2 = st.tabs(['📝Result', "📊Analysis"])

# --- Sidebar Login ---
st.sidebar.title("🔐 Teacher Login")
teacher_name = st.sidebar.text_input("👨‍🏫 Name").title().strip()
password = st.sidebar.text_input("🔐 Password", type="password").strip()

# --- State Setup ---
if "student_index" not in st.session_state:
    st.session_state.student_index = 0

if "save_clicked" not in st.session_state:
    st.session_state.save_clicked = False

if teacher_name and password:
    try:
        response_verify_teacher = requests.get(f"{API_URL}/verify_teacher/{teacher_name}/{password}")
        if response_verify_teacher.status_code == 200:
            result_verify_teacher = response_verify_teacher.json()
            if result_verify_teacher['status'] == 'success':
                teacher_class = result_verify_teacher['class']
                st.session_state.teacher_class = teacher_class
                st.sidebar.success(f"Welcome {teacher_name} 👨‍🏫 | Class: {teacher_class}")

                # Optional Camera
                image = st.sidebar.camera_input("📸 Take a photo for security")
                if image:
                    if not os.path.exists("teacher_images"):
                        os.makedirs("teacher_images")
                    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                    filename = f"teacher_images/{teacher_name.replace(' ', '_')}_{timestamp}.jpg"
                    with open(filename, "wb") as f:
                        f.write(image.getbuffer())
                    st.sidebar.success("📷 Image saved successfully!")

                logging.info(f"LOGIN SUCCESS - Name: {teacher_name}, Class: {teacher_class}")

                # === TAB 1: Result Entry ===
                with tab1:
                    response_students = requests.get(f"{API_URL}/show_students/{teacher_class}")
                    if response_students.status_code == 200:
                        students = response_students.json().get('students', [])
                        index = st.session_state.student_index

                        if index < len(students):
                            student = students[index]
                            st.subheader(f"👤 {student['name']} (Roll: {student['roll_num']})")

                            subjects = ['Maths', "Science", "English", "English Grammar",
                                        "Hindi", "Hindi Grammar", 'Social Science', "Art", "Computer"]
                            marks = {}

                            for sub in subjects:
                                col1, col2 = st.columns(2)
                                with col1:
                                    ext = st.number_input(f"{sub} External", 0, 80, key=f"{sub}_ext")
                                with col2:
                                    internal = st.number_input(f"{sub} Internal", 0, 20, key=f"{sub}_int")
                                marks[sub] = {"external": ext, "internal": internal}

                            if not st.session_state.save_clicked:
                                if st.button("✅ Save Result"):
                                    payload = {
                                        "student_name": student['name'],
                                        "roll_num": student['roll_num'],
                                        "class_name": teacher_class,
                                        "teacher_name": teacher_name,
                                        "marks": marks
                                    }
                                    response = requests.post(f"{API_URL}/add_to_result", json=payload)
                                    if response.status_code == 200:
                                        st.success(f"{student['name']}'s marks submitted!")
                                        st.balloons()
                                        st.session_state.save_clicked = True
                                        sleep(1)
                                        st.rerun()
                            else:
                                st.session_state.save_clicked = False
                                st.session_state.student_index += 1
                                sleep(1)
                                st.rerun()
                        else:
                            st.success("🎉 All students' results submitted.")
                    else:
                        st.error("⚠️ Couldn't fetch student list.")

                # === TAB 2: Analysis ===
                with tab2:
                    st.subheader("📈 All Submitted Results")
                    if st.button("📥 Show Class Results"):
                        teacher_class = st.session_state.get("teacher_class", None)
                        if teacher_class:
                            response_result = requests.get(f"{API_URL}/select_class/{teacher_class}")
                            if response_result.status_code == 200:
                                df = pd.DataFrame(response_result.json().get("students", []))
                                if not df.empty:
                                    st.dataframe(df)
                                else:
                                    st.warning("⚠️ No result data found.")
                            else:
                                st.error("🚫 Failed to fetch results.")
            else:
                st.sidebar.error("❌ Invalid credentials")
                logging.warning(f"LOGIN FAILED - Name: {teacher_name}")
        else:
            st.sidebar.error("⚠️ Server error. Try again later.")
    except requests.exceptions.ConnectionError:
        st.sidebar.error("🚫 Server is not reachable. Make sure FastAPI is running.")
else:
    st.sidebar.info("👈 Please enter your name and password.")
