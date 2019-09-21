from flask import Blueprint, current_app
from flask import abort
from flask import request
from flask import session

from app.mod_auth.models import check_user

mod_auth = Blueprint("auth", __name__, url_prefix="/auth")


@mod_auth.route("/login", methods=["POST"])
def login():
    uname = request.form.get("username", None)
    pw = request.form.get("password", None)

    if not uname or not pw:
        return "Missing username or password", 400

    ok, err = check_user(uname, pw)
    if not ok:
        return err, 403

    session["username"] = uname
    return "ok"


@mod_auth.route("/register", methods=["POST"])
def register():
    uname = request.form.get("username", None)
    pw = request.form.get("password", None)

    if not uname or not pw:
        return "Missing username or password", 400

    ok, err = register_user(username, password, 0)

    if not ok:
        return err, 400

    return "ok"
