import os
from flask import Flask
from models import db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

app.secret_key = os.environ.get("FLASK_SECRET_KEY", "changeme123")

from controllers import mod_auth

app.register_blueprint(mod_auth)

from views import views

app.register_blueprint(views)

if __name__ == "__main__":
    app.run("0.0.0.0", port=5000)
