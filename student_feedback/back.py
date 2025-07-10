from fastapi import FastAPI
from pydantic import  BaseModel
import db

app = FastAPI()


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


