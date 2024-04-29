from src.deps.db import db, QueryModel
import sqlalchemy as sa
from dataclasses import dataclass


@dataclass
class Game(QueryModel):
    __tablename__ = "games"

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(
        db.TIMESTAMP(timezone=True), server_default=sa.func.now(), nullable=False
    )
    name = db.Column(db.TEXT())

    league_id = db.Column(db.Integer, db.ForeignKey("sport_leagues.id"))
    first_team_id = db.Column(db.Integer, db.ForeignKey("teams.id"))
    second_team_id = db.Column(db.Integer, db.ForeignKey("teams.id"))
    sport_id = db.Column(db.Integer, db.ForeignKey("sports.id"))


@dataclass
class GameDetail(QueryModel):
    __tablename__ = "game_details"

    type = db.Column(db.TEXT())
    date = db.Column(db.DATE())
    start = db.Column(db.TIMESTAMP(timezone=True))
    end = db.Column(db.TIMESTAMP(timezone=True))
    games_id = db.Column(db.Integer, db.ForeignKey("games.id"), primary_key=True)


@dataclass
class GameScore(QueryModel):
    __tablename__ = "game_scores"

    id = db.Column(db.Integer, primary_key=True)
    total_score = db.Column(db.Integer())
    one_point = db.Column(db.Integer())
    two_points = db.Column(db.Integer())
    three_points = db.Column(db.Integer())
    four_points = db.Column(db.Integer())
    five_points = db.Column(db.Integer())
    six_points = db.Column(db.Integer())
    seven_points = db.Column(db.Integer())
    eight_points = db.Column(db.Integer())
    game_id = db.Column(db.Integer, db.ForeignKey("games.id"))
    team_id = db.Column(db.Integer, db.ForeignKey("teams.id"))
    player_id = db.Column(db.UUID, db.ForeignKey("user_profiles.uid"))
