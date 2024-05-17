from src.deps.db import db, QueryModel
import sqlalchemy as sa
from dataclasses import dataclass
# from src.models.athletes


@dataclass
class Sport(QueryModel):
    __tablename__ = "sports"

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(
        db.TIMESTAMP(timezone=True), server_default=sa.func.now(), nullable=False
    )
    name = db.Column(db.TEXT())
    description = db.Column(db.TEXT())

    teams = db.relationship("Team", back_populates="sport")
    # leagues = db.relationship("League", back_populates="sport")
    # organizations = db.relationship("Organization", back_populates="sport")


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
    sports_name = db.Column(db.TEXT())
    is_open = db.Column(db.BOOLEAN(), default=True)

    # sport = db.relationship("Sport", back_populates="leagues")


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

    teams = db.relationship("Team", back_populates="organization")
    # leagues = db.relationship("League", back_populates="organization")
    # sport = db.relationship("Sport", back_populates="organizations")

