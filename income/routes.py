from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from db.db import add_income, income_details

income_bp = Blueprint("income", __name__, url_prefix="/income")


@income_bp.route("/add", methods=["GET", "POST"])
def add():
   
    if "user_id" not in session:
        return redirect(url_for("users.login_user"))

    if request.method == "POST":
        amount = request.form.get("amount")
        source = request.form.get("source")
        date = request.form.get("date")

        success, message = add_income(
            session["user_id"],
            amount,
            source,
            date
        )

        flash(message, "success" if success else "error")

        if success:
            return redirect(url_for("income.list"))

    return render_template("income/create.html")


@income_bp.route("/list")
def list():
    # Protect route
    if "user_id" not in session:
        return redirect(url_for("users.login_user"))

    success, incomes = income_details(session["user_id"])

    if not success:
        flash(incomes, "error")
        incomes = []

    return render_template("income/list.html", incomes=incomes)