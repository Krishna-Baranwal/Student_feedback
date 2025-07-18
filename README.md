# 🎓 School Management System with Result Analysis and Feedback

Welcome to my **Full-Stack School Management System** project, designed for educational institutions to manage students, teachers, results, and feedbacks — all in one platform.
---
## 🛠️ Technologies Used

- **Frontend**: Streamlit (Python)
- **Backend**: FastAPI (Python)
- **Database**: MySQL
- **Data Analysis**: Pandas, Plotly
- **Utilities**: Requests, Logging, Camera Capture

---

## 🔑 Key Features

### 🧑‍💼 Admin Panel
- Admin login with secure access
- Add, View, Update, Delete:
  - ✅ Students
  - ✅ Teachers
- 📊 View class-wise student results
- 📉 Subject-wise average marks visualization (Bar Chart)
- 🥧 Pass vs Fail analysis (Pie Chart)
- 🗣️ View all feedbacks submitted by students
- 💸 Only students who have **paid full fees can view results**

### 👨‍🏫 Teacher Panel
- Teacher login (with class binding)
- Submit student marks (internal + external)
- Camera capture for login monitoring
- View submitted results for their class

### 🧑‍🎓 Student Panel
- Student login using name & password
- View personal results if dues are cleared
- User-friendly messages and alerts

### 🗣️ Feedback System
- Students can submit feedback
- Admin can view all feedbacks for improvement

---

## 🔐 Result Access Logic

- If a student has **not paid full fees**, their result is **restricted**.
- Ensures real-world logic and discipline for school fee compliance.

---

## 📂 Folder Structure
project/
│
├── backend.py # FastAPI backend
├── db.py # MySQL connection & queries
├── admin.py # Streamlit admin panel
├── teacher.py # Streamlit teacher panel
├── student.py # Streamlit student panel
├── login.log # Stores login activities
├── student_feedback/ # Feedback system backend
│ ├── back.py
│ ├── db.py
│ └── front.py
├── requirements.txt # Python dependencies
└── README.md

## 🚀 Getting Started

```bash
# 1. Clone the repo
git clone https://github.com/your-username/school-management-system.git
cd school-management-system

# 2. Setup virtual environment
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

# 3. Install requirements
pip install -r requirements.txt

# 4. Start FastAPI backend
uvicorn backend:app --reload

# 5. Start the Streamlit frontend
streamlit run admin.py
streamlit run teacher.py
streamlit run student.py


