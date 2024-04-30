from flask import Flask

from src.config import api_url_prefix


def register_blueprints(app: Flask):
    from src.deps import fairy_error
    from src.py_flask_vola.routers.api import auth, users, social
    from py_flask_vola.routers import signup

    app.register_blueprint(fairy_error.errors)

    # Routers/Controllers
    app.register_blueprint(signup.app, url_prefix="/")

    # API
    app.register_blueprint(
        auth.app, name="Authlog", url_prefix=f"{api_url_prefix}/auth"
    )
    app.register_blueprint(users.app, name="Users", url_prefix=f"{api_url_prefix}/users")
    app.register_blueprint(social.app, name="Social", url_prefix=f"{api_url_prefix}/")

    return app
