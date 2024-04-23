from apifairy import APIFairy
from flask import Flask

fairy = APIFairy()


def init_app(app: Flask) -> None:
    fairy.init_app(app)
