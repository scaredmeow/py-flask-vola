from flask import Blueprint
from src.models.social import Comment, Post
from src.deps.db import db
from src.decorators import paginated_response
from src.schemas import CommentSchema, OKRequestSchema, SocialPostSchema, PostSchema
from apifairy import body, response
from sqlalchemy.sql import text


app = Blueprint("Social", __name__)


@app.route("/posts", methods=["GET"])
@response(SocialPostSchema(many=True))
def get_all_posts():
    return Post.query.order_by(text("posts.created_at desc")).all()


@app.route("/posts/<int:post_id>", methods=["GET"])
@response(SocialPostSchema())
def get_specific_post(post_id: int):
    return Post.query.get(post_id)


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
@body(CommentSchema())
@response(OKRequestSchema)
def comment_post(data: dict, post_id: int):
    """Comment on a post"""
    comment = Comment(content=data.get("content"), user_id=data.get("user_id"), post_id=post_id)
    db.session.add(comment)
    db.session.commit()
    return {"description": "Comment added successfully"}


@app.route("/posts/<int:post_id>/comments", methods=["GET"])
@response(CommentSchema(many=True))
def get_post_comments(post_id: int):
    """Get comments on a post"""
    return Comment.query.filter_by(post_id=post_id).all()
