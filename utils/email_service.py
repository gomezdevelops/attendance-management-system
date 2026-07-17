from flask_mail import Message
from flask import current_app


def send_warning_email(email, student_name, subject_name, percentage):

    try:

        mail = current_app.extensions["mail"]

        msg = Message(
            subject="Attendance Warning",
            recipients=[email]
        )

        msg.body = f"""
Hello {student_name},

Your attendance for the subject {subject_name} has fallen below 75%.

Current Attendance: {percentage}%

Please attend classes regularly.

Smart Attendance System
"""

        mail.send(msg)

        print(
            f"Warning email sent to {student_name} "
            f"for subject {subject_name}"
        )

    except Exception as e:

        print("Email error:", e)

from flask_mail import Message
from flask import current_app


def send_report_email(email, student_id, report_text):

    try:

        mail = current_app.extensions["mail"]

        msg = Message(
            subject="Attendance Percentage Report",
            recipients=[email]
        )
        from datetime import datetime

        now = datetime.now()

        msg.body = f"""
Dear Student,

Here is your attendance percentage report:
Generated on: {now.strftime("%Y-%m-%d %H:%M")}
Student ID: {student_id}

{report_text}

Please maintain attendance above 75%.

-Smart Attendance System Admin
"""

        mail.send(msg)

        print("Report email sent to:", email)

    except Exception as e:

        print("Email error:", e)