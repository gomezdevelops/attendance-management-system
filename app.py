from flask import Flask
from database.db import create_tables
from routes.auth_routes import auth
from routes.student_routes import student
from routes.subject_routes import subject
from routes.attendance_routes import attendance
from flask_mail import Mail


app = Flask(__name__)
app.secret_key = "secret_key"

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True

app.config["MAIL_USERNAME"] = "attendancemailwarning@gmail.com"
app.config["MAIL_PASSWORD"] = "kyshbqzxvwkpswnl"


app.config["MAIL_DEFAULT_SENDER"] = "attendancemailwarning@gmail.com"
mail = Mail(app)

create_tables()

app.register_blueprint(auth)
app.register_blueprint(student)
app.register_blueprint(subject)
app.register_blueprint(attendance)

@app.after_request
def add_no_cache_headers(response):

    response.headers["Cache-Control"] = (
        "no-store, no-cache, must-revalidate, max-age=0"
    )

    response.headers["Pragma"] = "no-cache"

    response.headers["Expires"] = "0"

    return response

@app.route("/")
def home():
    return "Smart Attendance System Running"


if __name__ == "__main__":
    app.run(debug=True)