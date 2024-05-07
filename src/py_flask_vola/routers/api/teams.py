from flask import Blueprint
from src.models.athletes import Team, TeamMember
from src.deps.db import db
from src.decorators import paginated_response
from src.schemas import OKRequestSchema, TeamSchema, TeamMemberSchema, TeamsSchema
from apifairy import body, response

app = Blueprint("Teams", __name__)


@app.route("/", methods=["GET"])
@response(TeamsSchema)
def get_all_teams(data: dict):
    return Team.query.all()


@app.route("/", methods=["POST"])
@body(TeamSchema(exclude=("id", "created_at")))
@response(OKRequestSchema)
def create_team(data: dict):
    team = Team(name=data.get("name"), description=data.get("description"), sport_id=data.get("sport_id"))
    db.session.add(team)
    db.session.commit()

    team_member = TeamMember(user_id=data.get("user_id"), team_id=team.id, is_owner=True)
    db.session.add(team_member)
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

