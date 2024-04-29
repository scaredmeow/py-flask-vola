from src.deps.db import db, QueryModel
import sqlalchemy as sa
from dataclasses import dataclass


@dataclass
class Team(QueryModel):
    __tablename__ = "teams"

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(
        db.TIMESTAMP(timezone=True), server_default=sa.func.now(), nullable=False
    )
    name = db.Column(db.TEXT())
    description = db.Column(db.TEXT())
    sport_id = db.Column(db.Integer, db.ForeignKey("sports.id"))
    organization_id = db.Column(db.Integer, db.ForeignKey("sport_organizations.id"))


@dataclass
class TeamMember(QueryModel):
    __tablename__ = "team_members"

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(
        db.TIMESTAMP(timezone=True), server_default=sa.func.now(), nullable=False
    )
    team_id = db.Column(db.Integer, db.ForeignKey("teams.id"))
    user_id = db.Column(db.UUID, db.ForeignKey("user_profiles.uid"))
    league_id = db.Column(db.Integer, db.ForeignKey("sport_leagues.id"))
    organization_id = db.Column(db.Integer, db.ForeignKey("sport_organizations.id"))