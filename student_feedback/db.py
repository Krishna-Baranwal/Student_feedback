import mysql.connector.connection

cnx = mysql.connector.connect(
    user = 'root',
    password = 'root',
    database = 'feed',
    host= 'localhost'
)

cursor = cnx.cursor(dictionary=True)

def insert(student_name, subject, teacher_name, rating, comment):
    query=  """
    insert into feedback (student_name, subject, teacher_name, rating, comment) values(%s,%s,%s,%s,%s)
    """
    value = (student_name, subject, teacher_name, rating, comment)
    cursor.execute(query,value)
    cnx.commit()

def teacher_show():
    cursor.execute("Select teacher_name , subject from teachers")
    teacher = cursor.fetchall()
    return teacher

