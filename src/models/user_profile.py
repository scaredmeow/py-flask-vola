from src.deps.db import db, QueryModel
import sqlalchemy as sa
from dataclasses import dataclass


@dataclass
class User(QueryModel):
    __tablename__ = "user_profiles"
    __table_args__ = {"info": {"skip_autogenerate": True}}

    created_at = db.Column(db.TIMESTAMP, server_default=sa.func.now())
    uid = db.Column(db.UUID, primary_key=True)
    first_name = db.Column(db.TEXT())
    middle_name = db.Column(db.TEXT())
    last_name = db.Column(db.TEXT())
    email = db.Column(db.TEXT())
    gender = db.Column(db.TEXT())
    phone_number = db.Column(db.TEXT())
    birthdate = db.Column(db.DATE())
    role = db.Column(db.Integer, db.ForeignKey("user_roles.id"))

    active_role = db.relationship("Role", back_populates="profile")
    athlete_profile = db.relationship(
        "AthleteProfile", back_populates="profile", uselist=False
    )
    coach_profile = db.relationship(
        "CoachProfile", back_populates="profile", uselist=False
    )


@dataclass
class Role(QueryModel):
    __tablename__ = "user_roles"

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(
        db.TIMESTAMP(timezone=True), server_default=sa.func.now(), nullable=False
    )
    role_name = db.Column(db.TEXT())

    profile = db.relationship("User", back_populates="active_role", uselist=False)

    def __str__(self):
        return self.role_name


@dataclass
class AthleteProfile(QueryModel):
    __tablename__ = "user_profiles_athlete"

    uid = db.Column(db.UUID, db.ForeignKey("user_profiles.uid"), primary_key=True)
    created_at = db.Column(
        db.TIMESTAMP(timezone=True), server_default=sa.func.now(), nullable=False
    )
    civil_status = db.Column(db.TEXT())

    profile = db.relationship("User", back_populates="athlete_profile")


@dataclass
class CoachProfile(QueryModel):
    __tablename__ = "user_profiles_coach"

    uid = db.Column(db.UUID, db.ForeignKey("user_profiles.uid"), primary_key=True)
    created_at = db.Column(
        db.TIMESTAMP(timezone=True), server_default=sa.func.now(), nullable=False
    )
    organization = db.Column(db.TEXT, db.ForeignKey("sport_organizations.id"))
    team = db.Column(db.TEXT, db.ForeignKey("teams.id"))
    league = db.Column(db.TEXT, db.ForeignKey("sport_leagues.id"))

    profile = db.relationship("User", back_populates="coach_profile", uselist=False)


class ForeginKeyyWrapper(QueryModel):
    __tablename__ = "wrappers_fdw_stats"
    __table_args__ = {
        "info": {"skip_autogenerate": True},
        "comment": "Wrappers Foreign Data Wrapper statistics",
    }

    fdw_name = db.Column(db.String, primary_key=True)
