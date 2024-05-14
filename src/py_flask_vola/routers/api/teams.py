from flask import Blueprint
from src.models.athletes import Team, TeamMember, TrainingTasks, TrainingTasksProgress
from src.models.user_profile import User
from src.deps.db import db
from src.decorators import paginated_response
from src.schemas import HTTPRequestSchema, OKRequestSchema, TaskProgressSchema, TasksSchema, TeamMemberSchemaNormal, TeamSchema, TeamMemberSchema, TeamsSchema, WholeTasksSchema
from apifairy import body, response
from datetime import datetime

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

    team_member = TeamMember(user_id=data.get("user_id"), team_id=team.id, is_owner=True, pending=False)
    db.session.add(team_member)
    db.session.commit()

    user_obj = User.query.get(data.get("user_id"))

    user_obj.team_id = team.id
    db.session.commit()

    return {"description": "Team created successfully"}


@app.route("/<int:team_id>/accept", methods=["POST"])
@body(TeamMemberSchema(only=("user_id",)))
@response(OKRequestSchema)
def accept_team_request(args_data: dict, team_id: int):
    team_member = TeamMember.query.filter_by(user_id=args_data.get("user_id"), team_id=team_id).first()
    team_member.pending = False
    db.session.commit()
    return {"description": "User accepted successfully"}


@app.route("/<int:team_id>/reject", methods=["POST"])
@body(TeamMemberSchema(only=("user_id",)))
@response(OKRequestSchema)
def reject_team_request(args_data: dict, team_id: int):
    team_member = TeamMember.query.filter_by(user_id=args_data.get("user_id"), team_id=team_id).first()
    db.session.delete(team_member)
    db.session.commit()
    return {"description": "User rejected successfully"}


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


@app.route("/<int:team_id>/pending", methods=["GET"])
@response(TeamMemberSchemaNormal(many=True))
def get_pending_requests(team_id: int):
    return TeamMember.query.filter_by(team_id=team_id, pending=True).all()


@app.route("/tasks/<int:team_id>", methods=["GET"])
@response(WholeTasksSchema(many=True))
def get_team_tasks(team_id: int):
    return TrainingTasks.query.filter_by(team_id=team_id).all()


@app.route("/tasks/<int:team_id>", methods=["POST"])
@body(TasksSchema(exclude=("id", "created_at")))
@response(OKRequestSchema)
def create_team_tasks(data: dict, team_id: int):
    task = TrainingTasks(team_id=team_id, task_name=data.get("task_name"), task_description=data.get("task_description"), task_date=data.get("task_date") or datetime.now())
    db.session.add(task)
    db.session.commit()
    return {"description": "Task created successfully"}


@app.route("/tasks/<int:task_id>/complete", methods=["POST"])
@body(TaskProgressSchema(only=(["user_id"])))
@response(OKRequestSchema)
def complete_individual_tasks(data: dict, task_id: int):
    complete_task = TrainingTasksProgress(task_id=task_id, user_id=data.get("user_id"), task_status=True,
                                          team_id=TrainingTasks.query.get(task_id).team_id,
                                          team_member_id=TeamMember.query.filter_by(user_id=data.get("user_id")))
    db.session.add(complete_task)
    db.session.commit()
    return {"description": "Task completed successfully"}


@app.route("/tasks/athlete/<int:team_id>", methods=["POST"])
@body(TaskProgressSchema(only=(["user_id"])))
@response(WholeTasksSchema(many=True))
def get_athlete_tasks(data: dict, team_id: int):

    query_set = []

    for i in TrainingTasks.query.filter_by(team_id=team_id).all():
        if data.get("user_id") not in [abc.user_id for abc in i.progress]:
            query_set.append(i)
    return query_set


@app.route("/tasks/<int:team_id>/progress", methods=["GET"])
@response(HTTPRequestSchema())
def get_task_progress(team_id: int):

    number_of_tasks = len(TrainingTasks.query.filter_by(team_id=team_id).all())
    number_of_team_members = len(TeamMember.query.filter_by(team_id=team_id).all())
    number_of_completed_tasks = len(TrainingTasksProgress.query.filter_by(team_id=team_id, task_status=True).all())

    percentage = (number_of_completed_tasks / (number_of_tasks*number_of_team_members))
    return {"message": percentage}