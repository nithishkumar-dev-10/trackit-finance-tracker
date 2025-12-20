from db.db import balance
from flask import session, redirect, url_for,render_template
from flask import Blueprint

home_bp=Blueprint('home',__name__)

@home_bp.route("/")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("users.login_user"))

    success, data = balance(session["user_id"])

    if not success:
        data = {
            "total_income": 0,
            "total_expense": 0,
            "balance": 0
        }

    return render_template(
        "home/index.html",
        total_income=data["total_income"],
        total_expense=data["total_expense"],
        balance=data["balance"]
    )