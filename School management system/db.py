import mysql.connector


# Database Connection
cnx = mysql.connector.connect(
    user="root",
    password="root",
    host="localhost",
    database="full_school_system"
)
cursor = cnx.cursor(dictionary=True)

# Teacher functions
def verify_teacher(name , password):
    while cursor.nextset():
        pass
    cursor.execute("SELECT name,password,teacher_class FROM teachers WHERE name = %s AND password = %s", (name, password))
    result = cursor.fetchone()
    return result

def show_students(teacher_class):
    while cursor.nextset():
        pass
    cursor.execute("select name , roll_num from students where class = %s",(teacher_class,))
    result = cursor.fetchall()
    return result

def add_to_result(
    student_name, roll_num, class_name, teacher_name,
    maths_ext, maths_int,
    science_ext, science_int,
    english_ext, english_int,
    english_grammar_ext, english_grammar_int,
    hindi_ext, hindi_int,
    hindi_grammar_ext, hindi_grammar_int,
    sst_ext, sst_int,
    art_ext, art_int,
    computer_ext, computer_int
):
    total = (
        maths_ext + maths_int +
        science_ext + science_int +
        english_ext + english_int +
        english_grammar_ext + english_grammar_int +
        hindi_ext + hindi_int +
        hindi_grammar_ext + hindi_grammar_int +
        sst_ext + sst_int +
        art_ext + art_int +
        computer_ext + computer_int
    )

    percentage = (total / 600) * 100

    result_status = "Pass" if percentage >= 33 else "Fail"

    query = """
    INSERT INTO result (
        student_name, roll_num, student_class, teacher_name,
        maths_ext, maths_int,
        science_ext, science_int,
        english_ext, english_int,
        english_grammar_ext, english_grammar_int,
        hindi_ext, hindi_int,
        hindi_grammar_ext, hindi_grammar_int,
        social_science_ext, social_science_int,
        arts_ext, arts_int,
        computer_ext, computer_int,
        total, percentage, result_status
    ) VALUES (%s, %s, %s, %s, 
              %s, %s, %s, %s, 
              %s, %s, %s, %s, 
              %s, %s, %s, %s,
              %s, %s, %s, %s,
              %s, %s, %s, %s, %s)
    """

    values = (
        student_name, roll_num, class_name, teacher_name,
        maths_ext, maths_int,
        science_ext, science_int,
        english_ext, english_int,
        english_grammar_ext, english_grammar_int,
        hindi_ext, hindi_int,
        hindi_grammar_ext, hindi_grammar_int,
        sst_ext, sst_int,
        art_ext, art_int,
        computer_ext, computer_int,
        total, percentage, result_status
    )
    while cursor.nextset():
        pass
    cursor.execute(query, values)
    cnx.commit()
    return {"status": "success", "total": total, "percentage": percentage, "result": result_status}


def show_result(class_id):
    while cursor.nextset():
        pass
    cursor.execute("""
        SELECT r.student_name, r.roll_num,
               r.maths_ext, r.maths_int,
               r.science_ext, r.science_int,
               r.english_ext, r.english_int,
               r.english_grammar_ext, r.english_grammar_int,
               r.hindi_ext, r.hindi_int,
               r.hindi_grammar_ext, r.hindi_grammar_int,
               r.social_science_ext, r.social_science_int,
               r.arts_ext, r.arts_int,
               r.computer_ext, r.computer_int,
               r.total, r.percentage, r.result_status
        FROM result r
        JOIN students s ON r.roll_num = s.roll_num AND r.student_class = s.class
        WHERE r.student_class = %s AND (s.fees - s.fees_paid) < 1000
    """, (class_id,))

    result = cursor.fetchall()
    if not result:
        return {"result": []}  # ✅ Return empty safely

    return {"result": result}


# Student panel
def verify_student(name, password):
    while cursor.nextset():
        pass
    cursor.execute("""
        SELECT name, password, class AS class_id, roll_num 
        FROM students WHERE name = %s AND password = %s
    """, (name, password))
    result = cursor.fetchone()
    # print("🖨️ verify_student result:", result)
    return result

# Admin panel
def select_class(class_id):
    while cursor.nextset():
        pass
    cursor.execute("select * from result where student_class = %s",(class_id,))
    result = cursor.fetchall()
    return {"result": result}

def add_student(name, roll_num, class_id, fees, fees_paid, email, password):
    while cursor.nextset():
        pass
    query = """
    INSERT INTO students 
    (name, roll_num, class, fees, fees_paid, email, password)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    values = (name, roll_num, class_id, fees, fees_paid, email, password)
    cursor.execute(query, values)
    cnx.commit()
    return {"status": "success"}

def delete_student(name, class_id, roll_num):
    while cursor.nextset():
        pass
    query = """
    DELETE FROM students WHERE name = %s AND class = %s AND roll_num = %s
    """
    values = (name, class_id, roll_num)
    cursor.execute(query, values)
    cnx.commit()
    return {'status': 'success'}

def show_student(name, roll_num, class_id):
    while cursor.nextset():
        pass
    query = """
    SELECT * FROM students WHERE name = %s AND class = %s AND roll_num = %s
    """
    values = (name, class_id, roll_num)
    cursor.execute(query, values)
    result = cursor.fetchone()
    return {'status': 'success', 'result': result}

def add_teacher(name, email, password, teacher_class):
    while cursor.nextset():
        pass
    query = """
    INSERT INTO teachers (name, email, password, teacher_class)
    VALUES (%s, %s, %s, %s)
    """
    values = (name, email, password, teacher_class)
    cursor.execute(query, values)
    cnx.commit()
    return {"status": "success", "message": f"👨‍🏫 Teacher {name} added successfully!"}

def delete_teacher(name, teacher_class):
    while cursor.nextset():
        pass
    query = "DELETE FROM teachers WHERE name = %s AND teacher_class = %s"
    cursor.execute(query, (name, teacher_class))
    cnx.commit()
    return {"status": "success", "message": f"🗑️ Teacher {name} deleted successfully."}

def get_all_teachers():
    while cursor.nextset():
        pass
    query = "SELECT name, email, teacher_class FROM teachers"
    cursor.execute(query)
    result = cursor.fetchall()
    return result

def update_student(name, roll_num, class_id, email, password):
    while cursor.nextset():
        pass
    query = """
    UPDATE students
    SET email = %s, password = %s
    WHERE name = %s AND roll_num = %s AND class = %s
    """
    values = (email, password, name, roll_num, class_id)
    cursor.execute(query, values)
    cnx.commit()
    return {"status": "success", "message": f"🔄 Updated {name}'s details."}


def show_result_admin(class_id):
    while cursor.nextset():
        pass
    cursor.execute("""
        SELECT r.student_name, r.roll_num,
               r.maths_ext, r.maths_int,
               r.science_ext, r.science_int,
               r.english_ext, r.english_int,
               r.english_grammar_ext, r.english_grammar_int,
               r.hindi_ext, r.hindi_int,
               r.hindi_grammar_ext, r.hindi_grammar_int,
               r.social_science_ext, r.social_science_int,
               r.arts_ext, r.arts_int,
               r.computer_ext, r.computer_int,
               r.total, r.percentage, r.result_status
        FROM result r
        JOIN students s ON r.roll_num = s.roll_num AND r.student_class = s.class
        WHERE r.student_class = %s 
    """, (class_id,))
    result = cursor.fetchall()
    return {"result": result}


cnx2 = mysql.connector.connect(
    user = 'root',
    password = 'root',
    database = 'feed',
    host= 'localhost'
)

cursor2 = cnx2.cursor(dictionary=True)

def insert(student_name, subject, teacher_name, rating, comment):
    query=  """
    insert into feedback (student_name, subject, teacher_name, rating, comment) values(%s,%s,%s,%s,%s)
    """
    value = (student_name, subject, teacher_name, rating, comment)
    cursor2.execute(query,value)
    cnx2.commit()

def teacher_show():
    cursor2.execute("Select teacher_name , subject from teachers")
    teacher = cursor2.fetchall()
    return teacher


