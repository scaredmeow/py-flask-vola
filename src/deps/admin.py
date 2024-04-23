from flask import Flask
from flask_admin import Admin

admin = Admin(name="Admin", template_mode="bootstrap4")


def init_app(app: Flask) -> None:
    app.config["FLASK_ADMIN_SWATCH"] = "cerulean"
    admin.init_app(app)
