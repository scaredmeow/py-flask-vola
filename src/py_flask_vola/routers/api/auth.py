from flask import Blueprint
from marshmallow import INCLUDE
from src.schemas import HTTPRequestSchema, SignupSchema
from src.deps.supabase import supabase
from apifairy import body, response

app = Blueprint("auth", __name__)


@app.route("/signup", methods=["POST"])
@response(HTTPRequestSchema)
@body(SignupSchema(unknown=INCLUDE))
def signup(body_data: dict):
    """
    Signup
    """

    res = supabase.auth.sign_up(credentials={
        "email": body_data.get('email'),
        "password": body_data.get('password')}
    )

    return {
        "code": 200,
        "message": "OK",
        "description": res}
