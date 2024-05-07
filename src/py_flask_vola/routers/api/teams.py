from flask import Blueprint
from src.models.athletes import Team, TeamMember
from src.deps.db import db
from src.decorators import paginated_response
from src.schemas import OKRequestSchema, TeamSchema, TeamMemberSchema, TeamsSchema
from apifairy import body, response

app = Blueprint("Teams", __name__)


@app.route("/", methods=["GET"])
@paginated_response(TeamsSchema)
def get_all_teams(data: dict):
    return Team.query


@app.route("/", methods=["POST"])
@body(TeamSchema)
@response(OKRequestSchema)
def create_team(data: dict):
    team = Team(**data)
    db.session.add(team)
    db.session.commit()
    return {"description": "Team created successfully"}


@app.route("/<int:team_id>/join", methods=["POST"])
@body(TeamMemberSchema(only=("user_id",)))
@response(OKRequestSchema)
def join_team(args_data: dict, team_id: int):
    team_member = TeamMember(user_id=args_data.get("user_id"), team_id=team_id)
    db.session.add(team_member)
    db.session.commit()
    return {"description": "User joined successfully"}
