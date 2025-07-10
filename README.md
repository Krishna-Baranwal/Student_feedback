# 🎓 Student Feedback Collector App

This is a simple feedback collection system where students can give ratings and comments for teachers, built with **Python, FastAPI, MySQL, and Streamlit**.

---

## 🚀 Tech Stack Used

* 💻 Python 3.x
* ⚡ FastAPI (Backend)
* 🧠 MySQL (Database)
* 🌐 Streamlit (Frontend)
* 📦 Requests, Uvicorn, mysql-connector-python

---

## 📦 Requirements

### 🔧 Install these dependencies:

```bash
pip install fastapi streamlit uvicorn mysql-connector-python requests
```

---

## 🛠️ Setup Instructions

1. **Clone the repository**
2. Ensure MySQL is installed and running.
3. Create a database:

   ```sql
   CREATE DATABASE feedback;
   ```
4. Run backend server:

   ```bash
   uvicorn back:app --reload
   ```
5. Run frontend (UI):

   ```bash
   streamlit run front.py
   ```

---

## 🗃️ Database Tables Used

### `teachers` table:

```sql
CREATE TABLE teachers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    teacher_name VARCHAR(50),
    subject VARCHAR(50)
);
```

### `feedback` table:

```sql
CREATE TABLE feedback (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_name VARCHAR(50),
    subject VARCHAR(50),
    teacher_name VARCHAR(50),
    rating FLOAT,
    comment TEXT,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 📸 Features

* 📝 Students can submit feedback for teachers.
* 📊 Admins/Teachers can view average ratings and comments.
* 🎨 Simple UI made using Streamlit.

---

## 📁 Folder Structure

```
student_feedback_app/
├── front.py           # Streamlit frontend
├── back.py            # FastAPI backend
├── db.py              # MySQL connection logic
└── README.md          # Project setup and info
```

---

## 🙏 Credits

Made with 💛 by Krishna Baranwal\\
