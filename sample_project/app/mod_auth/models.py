import bcrypt
from app import db


class Base(db.Model):
    id = db.Column(db.Integer, primary_key=True)


class User(Base):
    __tablename__ = "auth_user"

    username = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(192), nullable=False)
    twofactor = db.Column(db.String(17), nullable=False)

    def __repr__(self):
        return "<User %s>" % (self.name)


def register_user(username, password, twofactor):
    if not username or not password:
        return False, "Missing username or password"

    user = User.query.filter_by(username=username).first()

    if user:
        return False, "User already exists"

    if len(password) < 6:
        return False, "Password too short"

    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    new_user = User(username=username, password=hashed, twofactor=twofactor)
    db.session.add(new_user)
    db.session.commit()

    return True, None


def check_user(username, password, twofactor):
    if not username or not password or not twofactor:
        return False, "Missing username or password or 2fa"

    user = (
        User.query.filter_by(username=username).filter_by(twofactor=twofactor).first()
    )
    if not user:
        return False, "User does not exist"

    if bcrypt.checkpw(password.encode("utf-8"), user.password):
        return True, None

    return False, "Incorrect password"
