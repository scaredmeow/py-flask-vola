from src.deps.db import db
import sqlalchemy as sa
from dataclasses import dataclass


@dataclass
class User(db.Model):
    __tablename__ = "user_infos"
    __table_args__ = {"info": {"skip_autogenerate": True}}

    created_at = db.Column(db.TIMESTAMP, server_default=sa.func.now())
    uid = db.Column(db.UUID, primary_key=True)
    first_name = db.Column(db.TEXT())
    last_name = db.Column(db.TEXT())
    email = db.Column(db.TEXT())
    gender = db.Column(db.TEXT())
    phone_number = db.Column(db.TEXT())
    role = db.Column(
        db.ForeignKey("user_roles.id")
    )

    current_role = db.relationship("Role", backref="user_infos")


class Role(db.Model):
    __tablename__ = "user_roles"

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.TIMESTAMP(timezone=True), server_default=sa.func.now(), nullable=False)
    role_name = db.Column(db.TEXT())

    def __str__(self):
        return self.role_name


class ForeginKeyyWrapper(db.Model):
    __tablename__ = "wrappers_fdw_stats"
    __table_args__ = {
        "info": {"skip_autogenerate": True},
        "comment": "Wrappers Foreign Data Wrapper statistics",
    }

    fdw_name = db.Column(db.String, primary_key=True)
