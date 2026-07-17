from flask import Blueprint, render_template, request, redirect, session, flash
from database.db import get_connection

subject = Blueprint("subject", __name__)


@subject.route("/subjects", methods=["GET", "POST"])
def manage_subjects():

    if "admin" not in session:
        return redirect("/login")

    conn = get_connection()
    cursor = conn.cursor()

    if request.method == "POST":

        subject_id = request.form["subject_id"]
        subject_name = request.form["subject_name"]
        department = request.form["department"]
        semester = request.form["semester"]

        try:

            cursor.execute("""
            INSERT INTO subjects
            (subject_id, subject_name, department, semester)
            VALUES (?, ?, ?, ?)
            """, (
                subject_id,
                subject_name,
                department,
                semester
            ))

            conn.commit()

            flash("Subject added successfully")

        except:

            flash("Subject ID already exists")

    cursor.execute("SELECT * FROM subjects")

    subjects = cursor.fetchall()

    conn.close()

    return render_template(
        "subjects.html",
        subjects=subjects
    )


@subject.route("/delete_subject/<subject_id>")
def delete_subject(subject_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT COUNT(*) FROM attendance
    WHERE subject_id = ?
    """, (subject_id,))

    count = cursor.fetchone()[0]

    if count > 0:
        conn.close()

        flash("Cannot delete subject. Attendance already exists for this subject.")

        return redirect("/subjects")

    cursor.execute("""
    DELETE FROM subjects
    WHERE subject_id = ?
    """, (subject_id,))

    conn.commit()
    conn.close()

    flash("Subject deleted successfully.")

    return redirect("/subjects")