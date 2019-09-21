import bcrypt
from functools import wraps
from flask import abort

from flask import session


def authn():
    return "username" in session


def login_required(f):
    @wraps(f)
    def decorated_func(*args, **kwargs):
        if not authn():
            return abort(401)

        return f(*args, **kwargs)

    return decorated_func
