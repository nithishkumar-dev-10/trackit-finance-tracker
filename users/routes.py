from flask import request, redirect, url_for, flash, session, render_template, Blueprint
from db.db import login, register

users_bp = Blueprint("users", __name__)

@users_bp.route("/login", methods=["GET", "POST"])
def login_user():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user_id = login(username, password)

        if user_id:
            session["user_id"] = user_id
            flash("Login successful", "success")
            return redirect(url_for("home.dashboard"))
        else:
            flash("Invalid username or password", "error")
            return redirect(url_for("users.login_user"))

    return render_template("users/login.html")


@users_bp.route("/register", methods=["GET", "POST"])
def register_user():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirm = request.form.get("confirm_password")

        if password != confirm:
            flash("Passwords do not match", "error")
            return redirect(url_for("users.register_user"))

        success, message = register(username, password)

        if success:
            flash(message, "success")
            return redirect(url_for("users.login_user"))
        else:
            flash(message, "error")
            return redirect(url_for("users.register_user"))

    return render_template("users/register.html")