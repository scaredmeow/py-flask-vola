from flask import Blueprint
from src.models.user_profile import User
from src.schemas import ProfileSchema
from src.deps.supabase import supabase
from src.deps.db import db
from apifairy import body, response

app = Blueprint("users", __name__)


@app.route("/get", methods=["POST"])
@body(ProfileSchema(only=["uid"]))
@response(ProfileSchema)
def get_one_user(data: dict):
    return User.query.filter_by(uid=data.get("uid")).first()


@app.route("/update", methods=["POST"])
@body(ProfileSchema(exclude=["email", "active_role", "created_at"]))
@response(ProfileSchema)
def update_user(data: dict):
    user = User.query.filter_by(uid=data.get("uid")).first()
    data.pop("uid")
    for key, value in data.items():
        setattr(user, key, value)
    db.session.commit()
    return user
