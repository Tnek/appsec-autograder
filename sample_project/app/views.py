from flask import Blueprint
from flask import current_app

views = Blueprint("views", __name__)


@views.route("/")
def index():
    return current_app.send_static_file("index.html")
