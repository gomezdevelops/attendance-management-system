from flask import Blueprint, render_template, request, redirect, session
from database.db import get_connection
from face_recognition_module.recognize_faces import recognize_and_mark_attendance
import pandas as pd


attendance = Blueprint("attendance", __name__)


@attendance.route("/attendance", methods=["GET", "POST"])
def start_attendance():

    if "admin" not in session:
        return redirect("/login")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM subjects")

    subjects = cursor.fetchall()

    conn.close()

    if request.method == "POST":

        subject_id = request.form["subject_id"]

        recognize_and_mark_attendance(subject_id)

    return render_template(
        "attendance.html",
        subjects=subjects
    )
@attendance.route("/view_attendance")
def view_attendance():

    if "admin" not in session:
        return redirect("/login")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            a.attendance_id,
            s.student_id,
            s.full_name,
            sub.subject_name,
            a.date,
            a.hour,
            a.status
        FROM attendance a
        JOIN students s
            ON a.student_id = s.student_id
        JOIN subjects sub
            ON a.subject_id = sub.subject_id
        ORDER BY a.date DESC
        """)

    records = cursor.fetchall()

    conn.close()

    return render_template(
        "view_attendance.html",
        records=records
    )
@attendance.route("/attendance_percentage")
def attendance_percentage():

    if "admin" not in session:
        return redirect("/login")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            s.student_id,
            s.full_name,
            sub.subject_name,

            COUNT(
                CASE 
                    WHEN a.status = 'Present' 
                    THEN 1 
                END
            ) AS attended_classes,

            (
                SELECT COUNT(DISTINCT date || hour)
                FROM attendance a2
                WHERE a2.subject_id = a.subject_id
            ) AS total_classes

        FROM attendance a

        JOIN students s
            ON a.student_id = s.student_id

        JOIN subjects sub
            ON a.subject_id = sub.subject_id

        GROUP BY 
            s.student_id,
            a.subject_id
        """)
    records = cursor.fetchall()

    percentage_data = []

    for row in records:

        student_id = row[0]
        full_name = row[1]
        subject_name = row[2]
        attended = row[3]
        total = row[4]

        if total == 0:
            percentage = 0
        else:
            percentage = round((attended / total) * 100, 2)

        percentage_data.append(
            (
                student_id,
                full_name,
                subject_name,
                attended,
                total,
                percentage
            )
        )

    conn.close()

    return render_template(
        "attendance_percentage.html",
        records=percentage_data
    )

from datetime import datetime


@attendance.route("/attendance_summary")
def attendance_summary():

    if "admin" not in session:
        return redirect("/login")

    today = datetime.now().strftime("%Y-%m-%d")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT

        sub.subject_name,

        SUM(
            CASE
                WHEN a.status = 'Present'
                THEN 1
                ELSE 0
            END
        ) AS present_count,

        SUM(
            CASE
                WHEN a.status = 'Absent'
                THEN 1
                ELSE 0
            END
        ) AS absent_count,

        COUNT(*) AS total_count

    FROM attendance a

    JOIN subjects sub
        ON a.subject_id = sub.subject_id

    WHERE a.date = ?

    GROUP BY sub.subject_name

    ORDER BY sub.subject_name
    """, (today,))

    records = cursor.fetchall()

    conn.close()

    return render_template(
        "attendance_summary.html",
        records=records,
        today=today
    )
@attendance.route("/export_excel")
def export_excel():

    if "admin" not in session:
        return redirect("/login")

    conn = get_connection()

    query = """
    SELECT 
        attendance.student_id,
        students.full_name,
        subjects.subject_name,
        attendance.date,
        attendance.hour,
        attendance.status
    FROM attendance
    JOIN students
        ON attendance.student_id = students.student_id
    JOIN subjects
        ON attendance.subject_id = subjects.subject_id
    """

    df = pd.read_sql_query(query, conn)

    file_path = "attendance_report.xlsx"

    df.to_excel(file_path, index=False)

    conn.close()

    from flask import send_file

    return send_file(
        file_path,
        as_attachment=True
    )

from utils.email_service import send_report_email


@attendance.route("/send_student_report", methods=["GET", "POST"])
def send_student_report():

    if "admin" not in session:
        return redirect("/login")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT student_id, full_name
    FROM students
    """)

    students = cursor.fetchall()

    if request.method == "POST":

        student_id = request.form["student_id"]

        # Get student email

        cursor.execute("""
        SELECT email
        FROM students
        WHERE student_id = ?
        """, (student_id,))

        email_record = cursor.fetchone()

        if not email_record:

            return "Student email not found"

        student_email = email_record[0]

        # Get attendance percentage

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

        report_lines = []

        for subject, attended, total in records:

            if total == 0:
                percentage = 0
            else:
                percentage = round(
                    (attended / total) * 100,
                    2
                )

            report_lines.append(
                f"{subject}: {percentage}%"
            )

        report_text = "\n".join(report_lines)

        send_report_email(
            student_email,
            student_id,
            report_text
        )

        conn.close()

        return "Report email sent successfully"

    conn.close()

    return render_template(
        "send_student_report.html",
        students=students
    )