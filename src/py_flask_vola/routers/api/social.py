from flask import Blueprint
from src.models.social import Post
from src.deps.db import db
from src.decorators import paginated_response
from src.schemas import OKRequestSchema, SocialPostSchema, PostSchema
from apifairy import body, response
from sqlalchemy.sql import text


app = Blueprint("Social", __name__)


@app.route("/posts", methods=["GET"])
@response(SocialPostSchema(many=True))
def get_all_posts():
    return Post.query.order_by(text("posts.created_at desc")).all()


@app.route("/posts/new", methods=["POST"])
@body(PostSchema(exclude=["id", "created_at", "likes"]))
@response(OKRequestSchema)
def create_post(data: dict):
    """Create new post"""

    post = Post(**data)
    db.session.add(post)
    db.session.commit()


@app.route("/posts/like", methods=["POST"])
@body(PostSchema(only=["id"]))
@response(OKRequestSchema)
def like_post(data: dict):
    """Like a post"""

    post = Post.query.get(data.get("id"))
    post.likes += 1
    db.session.commit()
    return {"description": "Post liked successfully"}


@app.route("/posts/unlike", methods=["POST"])
@body(PostSchema(only=["id"]))
@response(OKRequestSchema)
def unlike_post(data: dict):
    """Unlike a post"""

    post = Post.query.get(data.get("id"))
    post.likes -= 1
    db.session.commit()
    return {"description": "Post unliked successfully"}


@app.route("/posts/<int:post_id>/comment", methods=["POST"])
@body(PostSchema(only=["id", "comment"]))
@response(OKRequestSchema)
def comment_post(data: dict, post_id: int):
    """Comment on a post"""

    post = Post.query.get(post_id)
    post.comments.append(data.get("comment"))
    db.session.commit()
    return {"description": "Comment added successfully"}