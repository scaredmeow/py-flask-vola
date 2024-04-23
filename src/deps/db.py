from typing import TYPE_CHECKING, Type, TypeVar

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy.model import Model

M = TypeVar("M", bound="CompletionModel")


class CompletionModel(Model):
    @classmethod
    def cquery(cls: Type[M]):
        return cls.query


db = SQLAlchemy(model_class=CompletionModel)

if TYPE_CHECKING:
    BaseModel = db.make_declarative_base(CompletionModel)
else:
    BaseModel = db.Model

metadata = BaseModel.metadata
migrate = Migrate()


def init_app(app: Flask) -> None:
    db.init_app(app)

    migrate.init_app(app, db)
