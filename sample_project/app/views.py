from flask import Blueprint
from flask import current_app, request, render_template

views = Blueprint("views", __name__)


@views.route("/")
def index():
    return current_app.send_static_file("index.html")


@views.route("/spell_check", methods=["GET", "POST"])
def spell_check():
    if request.method == "POST":
        text = request.form.get("words")

    return render_template("spellcheck.html")
