from flask import Flask
from flask_marshmallow import Marshmallow

ma = Marshmallow()


def schema_name_resolver(schema):
    return schema.__module__ + "." + schema.__name__


def init_app(app: Flask) -> None:
    ma.init_app(app)
    ma.schema_name_resolver = schema_name_resolver
