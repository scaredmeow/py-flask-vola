from src.deps.db import db, QueryModel
import sqlalchemy as sa
from dataclasses import dataclass
from src.models.sports import Sport, League, Organization


@dataclass
class Team(QueryModel):
    __tablename__ = "teams"

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(
        db.TIMESTAMP(timezone=True), server_default=sa.func.now(), nullable=False
    )
    name = db.Column(db.TEXT())
    description = db.Column(db.TEXT())
    image = db.Column(db.TEXT())
    sport_id = db.Column(db.Integer, db.ForeignKey("sports.id"))
    organization_id = db.Column(db.Integer, db.ForeignKey("sport_organizations.id"))

    team_members = db.relationship("TeamMember", back_populates="team")
    sport = db.relationship("Sport", back_populates="teams")
    organization = db.relationship("Organization", back_populates="teams")


@dataclass
class TeamMember(QueryModel):
    __tablename__ = "team_members"

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(
        db.TIMESTAMP(timezone=True), server_default=sa.func.now(), nullable=False
    )
    team_id = db.Column(db.Integer, db.ForeignKey("teams.id"))
    is_owner = db.Column(db.BOOLEAN(), default=False)
    user_id = db.Column(db.UUID, db.ForeignKey("user_profiles.uid"))
    pending = db.Column(db.BOOLEAN(), default=True)
    # league_id = db.Column(db.Integer, db.ForeignKey("sport_leagues.id"))
    # organization_id = db.Column(db.Integer, db.ForeignKey("sport_organizations.id"))
    team = db.relationship("Team", back_populates="team_members")
    user = db.relationship("User", back_populates="teams")


@dataclass
class TeamStats(QueryModel):
    __tablename__ = "team_stats"

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(
        db.TIMESTAMP(timezone=True), server_default=sa.func.now(), nullable=False
    )
    team_id = db.Column(db.Integer, db.ForeignKey("teams.id"))
    league_id = db.Column(db.Integer, db.ForeignKey("sport_leagues.id"))
    organization_id = db.Column(db.Integer, db.ForeignKey("sport_organizations.id"))
    win = db.Column(db.Integer())
    loss = db.Column(db.Integer())
    draw = db.Column(db.Integer())


@dataclass
class PlayerStats(QueryModel):
    __tablename__ = "player_stats"

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(
        db.TIMESTAMP(timezone=True), server_default=sa.func.now(), nullable=False
    )
    user_id = db.Column(db.UUID, db.ForeignKey("user_profiles.uid"))
    team_id = db.Column(db.Integer, db.ForeignKey("teams.id"))
    stats_key = db.Column(db.TEXT())
    stats_value = db.Column(db.TEXT())

    user = db.relationship("User", back_populates="stats")