from flask import Blueprint, render_template, request, session, redirect, url_for
from db.db import monthly_summary

summary_bp = Blueprint("summary", __name__, url_prefix="/summary")


@summary_bp.route("/", methods=["GET", "POST"])
def monthly():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    data = None
    has_data = False
    error = None

    if request.method == "POST":
        year = request.form["year"]
        month = request.form["month"]

        success, result = monthly_summary(
            session["user_id"],
            year,
            month
        )

        if success:
            data = result
            has_data = True
        else:
            error = result

    return render_template(
        "summary/monthly.html",
        data=data,
        has_data=has_data,
        error=error
    )