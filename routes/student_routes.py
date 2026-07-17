from flask import Blueprint, render_template, request, redirect, session, flash
from database.db import get_connection
from werkzeug.security import generate_password_hash, check_password_hash
from face_recognition_module.capture_faces import capture_face
from utils.email_service import send_warning_email

student = Blueprint("student", __name__)




@student.route("/register_student", methods=["GET", "POST"])
def register_student():

    if "admin" not in session:
        return redirect("/login")

    if request.method == "POST":

        student_id = request.form["student_id"]
        full_name = request.form["full_name"]
        department = request.form["department"]
        semester = request.form["semester"]
        email = request.form["email"]

        password = "student123"
        password_hash = generate_password_hash(password)

        conn = get_connection()
        cursor = conn.cursor()

        try:

            cursor.execute("""
            INSERT INTO students
            (student_id, full_name, department, semester, email, password_hash)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (
                student_id,
                full_name,
                department,
                semester,
                email,
                password_hash
            ))

            conn.commit()

            flash("Student registered successfully! Capturing face now...")

            print("Calling capture_face function...")
            print("DEBUG: About to capture face for", student_id)

            capture_face(student_id)

        except:

            flash("Student ID already exists.")

        conn.close()

    return render_template("register_student.html")



@student.route("/student_login", methods=["GET", "POST"])
def student_login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT student_id, password_hash
        FROM students
        WHERE email = ?
        """, (email,))

        record = cursor.fetchone()

        conn.close()

        if record:

            student_id = record[0]
            password_hash = record[1]

            if check_password_hash(password_hash, password):

                session["student"] = student_id

                return redirect("/student_dashboard")

        flash("Invalid email or password")

    return render_template("student_login.html")




@student.route("/student_dashboard")
def student_dashboard():

    if "student" not in session:
        return redirect("/student_login")

    return render_template("student_dashboard.html")




@student.route("/my_percentage")
def my_percentage():

    if "student" not in session:
        return redirect("/student_login")

    student_id = session["student"]

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT full_name, email
    FROM students
    WHERE student_id = ?
    """, (student_id,))

    student_record = cursor.fetchone()

    student_name = student_record[0]
    student_email = student_record[1]

    cursor.execute("""
    SELECT 
        sub.subject_name,

        COUNT(
            CASE 
                WHEN status = 'Present'
                THEN 1
            END
        ) AS attended,

        COUNT(DISTINCT date || hour) AS total

    FROM attendance a

    JOIN subjects sub
        ON a.subject_id = sub.subject_id

    WHERE student_id = ?

    GROUP BY sub.subject_name
    """, (student_id,))

    records = cursor.fetchall()

    percentage_data = []

    for subject, attended, total in records:

        if total == 0:
            percentage = 0
        else:
            percentage = round((attended / total) * 100, 2)
        warning = ""

        if percentage < 75:

            warning = "⚠ Low Attendance"

            if student_email:

                if "warning_sent" not in session:

                    from utils.email_service import send_warning_email

                    send_warning_email(
                        student_email,
                        student_name,
                        subject,
                        percentage
                    )

                    print("Email sent to:", student_email)

                    session["warning_sent"] = True

        percentage_data.append(
            (
                subject,
                attended,
                total,
                percentage,
                warning
            )
        )

    conn.close()

    return render_template(
        "student_percentage.html",
        records=percentage_data
    )


@student.route("/student_logout")
def student_logout():

    session.clear()

    return redirect("/student_login")

@student.route("/delete_student", methods=["GET", "POST"])
def delete_student():

    if "admin" not in session:
        return redirect("/login")

    conn = get_connection()
    cursor = conn.cursor()

    if request.method == "POST":

        student_id = request.form["student_id"]

        try:

            # Delete attendance first
            cursor.execute("""
            DELETE FROM attendance
            WHERE student_id = ?
            """, (student_id,))

            # Delete face encoding
            cursor.execute("""
            DELETE FROM face_encodings
            WHERE student_id = ?
            """, (student_id,))

            # Delete student
            cursor.execute("""
            DELETE FROM students
            WHERE student_id = ?
            """, (student_id,))

            conn.commit()

            flash("Student deleted successfully.")

        except Exception as e:

            flash("Error deleting student.")

        return redirect("/dashboard")

    cursor.execute("""
    SELECT student_id, full_name
    FROM students
    """)

    students = cursor.fetchall()

    conn.close()

    return render_template(
        "delete_student.html",
        students=students
    )