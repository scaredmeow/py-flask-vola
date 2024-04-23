from flask import (
    Blueprint,
    flash,
    render_template,
    request,
    redirect,
    stream_template,
    url_for,
    session,
)
from flask_admin.babel import gettext
from src.deps.supabase import supabase

app = Blueprint("auth", __name__)


@app.route("/signup", methods=["POST"])
def signup():
    """
    Signup
    """
    email = request.form.get("email")
    password = request.form.get("password")

    if not email or not password:
        flash(gettext('Failed to delete user', error=str("Error")), 'error')

    try:
        supabase.auth.sign_up(credentials={
            "email": email,
            "password": password}
        )
        flash(gettext('User created successfully.'), 'success')
    except Exception as ex:
        flash(gettext('Failed to create user', error=str(ex)), 'error')

    return redirect(url_for("admin.index"))
