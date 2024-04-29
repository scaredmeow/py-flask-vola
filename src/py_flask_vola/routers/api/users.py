from flask import Blueprint
from src.models.user_profile import User
from src.schemas import ProfileSchema
from apifairy import body, response

app = Blueprint("users", __name__)


@app.route("/get", methods=["POST"])
@body(ProfileSchema(only=["uid"]))
@response(ProfileSchema)
def get_one_user(data: dict):
    return User.query.filter_by(uid=data.get("uid")).first()
