from flask import Flask

from src.config import api_url_prefix


def register_blueprints(app: Flask):
    from src.deps import fairy_error

    app.register_blueprint(fairy_error.errors)

    # Routers/Controllers

    # API

    return app
