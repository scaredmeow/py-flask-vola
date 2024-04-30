from flask import Blueprint
from src.models.social import Post
from src.decorators import paginated_response
from src.schemas import SocialPostSchema, PostSchema
from apifairy import body, response

app = Blueprint("Social", __name__)


@app.route("/posts", methods=["GET"])
@paginated_response(SocialPostSchema)
def get_all_posts(data: dict):
    return Post.query
