from flask import Blueprint
from src.models.social import Post
from src.deps.db import db
from src.decorators import paginated_response
from src.schemas import OKRequestSchema, SocialPostSchema, PostSchema
from apifairy import body, response

app = Blueprint("Social", __name__)


@app.route("/posts", methods=["GET"])
@response(SocialPostSchema(many=True))
def get_all_posts():
    return Post.query.all()


@app.route("/posts/new", methods=["POST"])
@body(PostSchema(exclude=["id", "created_at", "likes"]))
@response(OKRequestSchema)
def create_post(data: dict):
    """Create new post"""

    post = Post(**data)
    db.session.add(post)
    db.session.commit()

