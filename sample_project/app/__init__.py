import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)

app.secret_key = os.environ.get("FLASK_SECRET_KEY", "changeme123")

from app.mod_auth.controllers import mod_auth as auth_module

app.register_blueprint(auth_module)

from app.views import views

app.register_blueprint(views)

db.create_all()
