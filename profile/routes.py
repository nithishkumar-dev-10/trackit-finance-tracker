from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash
)

from db.db import get_user_by_id, change_password

profile_bp = Blueprint(
    "profile",
    __name__,
    url_prefix="/profile"
)


@profile_bp.route("/", methods=["GET"])
def view_profile():
    if "user_id" not in session:
        flash("Please login to access your profile", "warning")
        return redirect(url_for("users.login_user"))

    user = get_user_by_id(session["user_id"])

    if not user:
        flash("User not found", "error")
        return redirect(url_for("users.login_user"))

    return render_template(
        "profile/profile.html",
        user=user
    )


@profile_bp.route("/change-password", methods=["POST"])
def update_password():
    if "user_id" not in session:
        flash("Please login again", "warning")
        return redirect(url_for("users.login_user"))

    old_password = request.form.get("old_password")
    new_password = request.form.get("new_password")
    confirm_password = request.form.get("confirm_password")

    if not old_password or not new_password or not confirm_password:
        flash("All fields are required", "error")
        return redirect(url_for("profile.view_profile"))

    if new_password != confirm_password:
        flash("New passwords do not match", "error")
        return redirect(url_for("profile.view_profile"))

    success, message = change_password(
        session["user_id"],
        old_password,
        new_password
    )

    flash(message, "success" if success else "error")
    return redirect(url_for("profile.view_profile"))


@profile_bp.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out", "info")
    return redirect(url_for("users.login_user"))