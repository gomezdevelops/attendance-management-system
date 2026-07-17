from flask import Blueprint, render_template, request, redirect, session, flash
from database.db import get_connection
from werkzeug.security import check_password_hash

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM admins WHERE username = ?",
            (username,)
        )

        admin = cursor.fetchone()

        conn.close()

        if admin and check_password_hash(admin[2], password):

            session["admin"] = admin[1]

            return redirect("/dashboard")

        else:

            flash("Invalid username or password")

    return render_template("login.html")


@auth.route("/dashboard")
def dashboard():

    if "admin" not in session:

        return redirect("/login")

    return render_template("dashboard.html")


@auth.route("/logout")
def logout():

    session.clear()

    return redirect("/login")