from app import db


class Base(db.Model):
    id = db.Column(db.Integer, primary_key=True)


class User(Base):
    __tablename__ = "auth_user"

    name = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(192), nullable=False)
    role = db.Column(db.SmallInteger, nullable=False)

    def __repr__(self):
        return "<User %s>" % (self.name)


def register_user(username, password, role):
    user = User.query.filter_by(username=username).first()

    if user:
        return False, "User already exists"

    if len(password) < 6:
        return False, "Password too short"

    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    new_user = User(username=username, password=hashed, role=role)
    db.session.add(new_user)
    db.session.commit()

    return True, None


def check_user(username, password):
    user = User.query.filter_by(username=username).first()
    if not user:
        return False, "User does not exist"

    if bcrypt.checkpw(password.encode("utf-8"), user.password):
        return True, None

    return False, "Incorrect password"


def check_permission(username, role):
    user = User.query.filter_by(username=username).first()

    if not user:
        return False, "User does not exist"

    return role <= user.role, None


def update_permission(username, to_update_name, role):
    ok, err = check_permission(username, role)
    if not ok:
        return False, err

    updated_user = User.query.filter_by(username=to_update_name).first()
    updated_user.role = role
    db.session.commit()
    return True, None
