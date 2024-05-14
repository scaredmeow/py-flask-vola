from flask import Blueprint
from src.models.athletes import Team, TeamMember
from src.models.user_profile import User
from src.deps.db import db
from src.decorators import paginated_response
from src.schemas import OKRequestSchema, TeamSchema, TeamMemberSchema, TeamsSchema
from apifairy import body, response

app = Blueprint("Teams", __name__)


@app.route("/", methods=["GET"])
@response(TeamsSchema(many=True))
def get_all_teams():
    return Team.query.all()


@app.route("/<int:team_id>", methods=["GET"])
@response(TeamsSchema())
def get_specific_teams(team_id: int):
    return Team.query.get(team_id)


@app.route("/", methods=["POST"])
@body(TeamSchema(exclude=("id", "created_at")))
@response(OKRequestSchema)
def create_team(data: dict):
    team = Team(name=data.get("name"),
                description=data.get("description"),
                sport_id=data.get("sport_id"),
                image=data.get("image"))
    db.session.add(team)
    db.session.commit()

    team_member = TeamMember(user_id=data.get("user_id"), team_id=team.id, is_owner=True)
    db.session.add(team_member)
    db.session.commit()

    user_obj = User.query.get(data.get("user_id"))

    user_obj.team_id = team.id
    db.session.commit()

    return {"description": "Team created successfully"}


@app.route("/<int:team_id>/join", methods=["POST"])
@body(TeamMemberSchema(only=("user_id",)))
@response(OKRequestSchema)
def join_team(args_data: dict, team_id: int):
    team_member = TeamMember(user_id=args_data.get("user_id"), team_id=team_id)
    db.session.add(team_member)
    db.session.commit()

    user_obj = User.query.get(args_data.get("user_id"))

    user_obj.team_id = team_id
    db.session.commit()
    return {"description": "User joined successfully"}


@app.route("/<int:team_id>/leave", methods=["POST"])
@body(TeamMemberSchema(only=("user_id",)))
@response(OKRequestSchema)
def leave_team(args_data: dict, team_id: int):
    team_member = TeamMember.query.filter_by(user_id=args_data.get("user_id"), team_id=team_id).first()
    db.session.delete(team_member)
    db.session.commit()

    user_obj = User.query.get(args_data.get("user_id"))

    user_obj.team_id = None
    db.session.commit()
    return {"description": "User left the team successfully"}