from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict
import db

app = FastAPI(title="📘 School Management System API", description="FastAPI backend with emojis", version="1.0")

# 📦 Data Models
class SubjectMarks(BaseModel):
    external: int
    internal: int

class Teacher(BaseModel):
    name: str
    email: str
    password: str
    teacher_class: int

class TeacherDelete(BaseModel):
    name: str
    teacher_class: int

class ResultEntry(BaseModel):
    student_name: str
    roll_num: int
    class_name: int
    teacher_name: str
    marks: Dict[str, SubjectMarks]

class StudentData(BaseModel):
    name: str
    roll_num: int
    class_id: int
    fees: int
    fees_paid: int
    email: str
    password: str

class StudentDelete(BaseModel):
    name: str
    class_id: int
    roll_num: int

class StudentUpdate(BaseModel):
    name: str
    roll_num: int
    class_id: int
    email: str
    password: str

# ============================
# 👨‍🏫 TEACHER ROUTES
# ============================

@app.get("/verify_teacher/{teacher}/{password}")
def verify_teacher(teacher: str, password: str):
    result = db.verify_teacher(teacher, password)
    if result:
        return {
            "status": "success",
            "teacher_name": result["name"],
            "class": result["teacher_class"]
        }
    return {"status": "error", "message": "❌ Invalid teacher credentials."}

@app.get("/show_students/{student_class}")
def show_students(student_class: int):
    result = db.show_students(student_class)
    return {"students": result}

@app.post("/add_to_result")
def add_to_result(data: ResultEntry):
    m = data.marks
    return db.add_to_result(
        student_name=data.student_name,
        roll_num=data.roll_num,
        class_name=data.class_name,
        teacher_name=data.teacher_name,
        maths_ext=m["Maths"].external, maths_int=m["Maths"].internal,
        science_ext=m["Science"].external, science_int=m["Science"].internal,
        english_ext=m["English"].external, english_int=m["English"].internal,
        english_grammar_ext=m["English Grammar"].external, english_grammar_int=m["English Grammar"].internal,
        hindi_ext=m["Hindi"].external, hindi_int=m["Hindi"].internal,
        hindi_grammar_ext=m["Hindi Grammar"].external, hindi_grammar_int=m["Hindi Grammar"].internal,
        sst_ext=m["Social Science"].external, sst_int=m["Social Science"].internal,
        art_ext=m["Art"].external, art_int=m["Art"].internal,
        computer_ext=m["Computer"].external, computer_int=m["Computer"].internal
    )

@app.get("/show_result/{class_id}")
def result_show(class_id: int):
    return db.show_result(class_id) or {"result": []}

# ============================
# 🎓 STUDENT ROUTES
# ============================

@app.get("/verify_student/{student_name}/{student_password}")
def verify_student_route(student_name: str, student_password: str):
    result = db.verify_student(student_name, student_password)
    if result:
        return {
            "status": "success",
            "name": result["name"],
            "class_id": result["class_id"],
            "password": result["password"],
            "roll_num": result["roll_num"]
        }
    return {"status": "error", "message": "❌ Invalid student credentials."}


@app.get("/show")
def show_teachers():
    return db.teacher_show()


class Info(BaseModel):
    name : str
    standard : int
    teacher_name : str
    teacher_subject : str
    comment : str
    rating : float


@app.post("/submit_form")
def student_feed(info : Info):
    db.insert(
        student_name=info.name,
        subject=info.teacher_subject,
        teacher_name=info.teacher_name,
        rating=info.rating,
        comment=info.comment
    )





# ============================
# 🧑‍💼 ADMIN ROUTES
# ============================

@app.get("/select_class/{class_id}")
def show_result_to_admin(class_id: int):
    result = db.show_result_admin(class_id)
    return {"status": "success", "students": result["result"]} if result else {"status": "error", "students": []}

@app.post("/add_student")
def add_student_route(student: StudentData):
    db.add_student(
        student.name, student.roll_num, student.class_id,
        student.fees, student.fees_paid, student.email, student.password
    )
    return {"status": "success", "message": f"🧑‍🎓 Student {student.name} added successfully."}

@app.post("/delete_student")
def delete_student_route(student: StudentDelete):
    db.delete_student(student.name, student.class_id, student.roll_num)
    return {"status": "success", "message": f"🗑️ Student {student.name} deleted successfully."}

@app.get("/show_student")
def show_student(name: str, roll_num: int, class_id: int):
    result = db.show_student(name, roll_num, class_id)
    return {"status": "success", "result": result}

@app.post("/add_teacher")
def route_add_teacher(teacher: Teacher):
    return db.add_teacher(
        name=teacher.name,
        email=teacher.email,
        password=teacher.password,
        teacher_class=teacher.teacher_class
    )

@app.post("/delete_teacher")
def route_delete_teacher(teacher: TeacherDelete):
    return db.delete_teacher(
        name=teacher.name,
        teacher_class=teacher.teacher_class
    )

@app.get("/show_teachers")
def route_show_teachers():
    teachers = db.get_all_teachers()
    return {"status": "success", "teachers": teachers, "message": "📋 All teachers fetched successfully."}



@app.post("/update_student")
def update_student_route(data: StudentUpdate):
    return db.update_student(data.name, data.roll_num, data.class_id, data.email, data.password)
