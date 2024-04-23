import os

from flask import Flask

from src.config import Config
from src.deps import blueprint, db, fairy, ma, admin, supabase
from utils import import_name


def create_app(config=Config) -> Flask:
    app = Flask(__name__)

    app.config.from_object(config)
    app.secret_key = os.urandom(24)

    # Initialize dependencies
    db.init_app(app)
    ma.init_app(app)
    fairy.init_app(app)
    admin.init_app(app)
    supabase.init_app(app)

    # Register blueprints
    blueprint.register_blueprints(app)

    # Register models
    for model in os.listdir("src/models"):
        if model != "__init__.py" and model.endswith(".py"):
            import_name("src.models", model.replace(".py", ""))

    # Register Admin
    from src.py_flask_vola.routers import admin as admin_router  # noqa

    return app
