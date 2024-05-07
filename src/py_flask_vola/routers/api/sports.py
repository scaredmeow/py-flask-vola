from flask import Blueprint
from src.models.sports import Sport
# from src.deps.db import db
# from src.decorators import paginated_response
from src.schemas import SportSchema
from apifairy import response

app = Blueprint("Sports", __name__)


@app.route("/", methods=["GET"])
@response(SportSchema(many=True))
def get_all_sports():
    """Get all sports"""

    return Sport.query.all()
