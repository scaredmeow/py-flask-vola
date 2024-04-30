from src.deps.db import db, QueryModel
import sqlalchemy as sa
from dataclasses import dataclass


@dataclass
class Post(QueryModel):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(
        db.TIMESTAMP(timezone=True), server_default=sa.func.now(), nullable=False
    )
    title = db.Column(db.TEXT)
    content = db.Column(db.TEXT)
    user_id = db.Column(db.UUID, db.ForeignKey("user_profiles.uid"))
    likes = db.Column(db.Integer, server_default="0")
    image = db.Column(db.TEXT)

    user = db.relationship("User", back_populates="posts")
    comments = db.relationship("Comment", back_populates="post")

    def __str__(self):
        return self.title


@dataclass
class Comment(QueryModel):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(
        db.TIMESTAMP(timezone=True), server_default=sa.func.now(), nullable=False
    )
    content = db.Column(db.TEXT)
    user_id = db.Column(db.UUID, db.ForeignKey("user_profiles.uid"))
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"))

    post = db.relationship("Post", back_populates="comments")
    user = db.relationship("User", back_populates="comments")

    def __str__(self):
        return f"<Comment {self.id}>"
