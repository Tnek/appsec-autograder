from flask import Blueprint, current_app
from flask import abort, request, session, render_template, redirect, url_for

from .models import check_user, register_user

mod_auth = Blueprint("auth", __name__)


@mod_auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        uname = request.form.get("uname", None)
        pw = request.form.get("pword", None)
        twofactor = request.form.get("2fa", None)

        ok, err = check_user(uname, pw, twofactor)
        if not ok or err is not None:
            session["username"] = uname
            return render_template("login.html", error=err)
        return redirect("/")

    return render_template("login.html")


@mod_auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        uname = request.form.get("uname", None)
        pw = request.form.get("pword", None)
        twofactor = request.form.get("2fa", None)
        ok, err = register_user(uname, pw, twofactor)

        if not ok or err is not None:
            return render_template("register.html", error=err)
        return redirect(url_for("auth.login"))

    return render_template("register.html")


@mod_auth.route("/logout")
def logout():
    if "username" in session:
        del session["username"]
    return redirect(url_for("auth.login"))
