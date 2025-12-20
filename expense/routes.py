from flask import Blueprint, render_template, request, redirect, session, url_for
from db.db import add_expense, expense_details, delete_expense

expense_bp = Blueprint("expense", __name__, url_prefix="/expense")


@expense_bp.route("/create", methods=["GET", "POST"])
def create():
    if "user_id" not in session:
        return redirect(url_for("users.login_user"))

    if request.method == "POST":
        amount = request.form["amount"]
        date = request.form["date"]
        purpose = request.form["purpose"]

        success, msg = add_expense(
            session["user_id"],
            amount,
            date,
            purpose
        )

        if success:
            return redirect(url_for("expense.list"))
        else:
            return render_template("expense/create.html", error=msg)

    return render_template("expense/create.html")


@expense_bp.route("/list")
def list():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    success, expenses = expense_details(session["user_id"])
    if not success:
        expenses = []

    return render_template("expense/list.html", expenses=expenses)


@expense_bp.route("/delete/<int:expense_id>")
def delete(expense_id):
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    delete_expense(session["user_id"], expense_id)
    return redirect(url_for("expense.list"))