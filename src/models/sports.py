from src.deps.db import db, QueryModel
import sqlalchemy as sa
from dataclasses import dataclass


@dataclass
class Sport(QueryModel):
    __tablename__ = "sports"

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(
        db.TIMESTAMP(timezone=True), server_default=sa.func.now(), nullable=False
    )
    name = db.Column(db.TEXT())
    description = db.Column(db.TEXT())


@dataclass
class League(QueryModel):
    __tablename__ = "sport_leagues"

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(
        db.TIMESTAMP(timezone=True), server_default=sa.func.now(), nullable=False
    )
    name = db.Column(db.TEXT())
    description = db.Column(db.TEXT())
    sport_id = db.Column(db.Integer, db.ForeignKey("sports.id"))
    is_open = db.Column(db.BOOLEAN(), default=True)


@dataclass
class Organization(QueryModel):
    __tablename__ = "sport_organizations"

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(
        db.TIMESTAMP(timezone=True), server_default=sa.func.now(), nullable=False
    )
    name = db.Column(db.TEXT())
    description = db.Column(db.TEXT())
    sport_id = db.Column(db.Integer, db.ForeignKey("sports.id"))