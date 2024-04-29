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
    title = db.Column(db.TEXT())
    content = db.Column(db.TEXT())
    user_id = db.Column(db.UUID, db.ForeignKey("user_profiles.uid"))


@dataclass
class Comment(QueryModel):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(
        db.TIMESTAMP(timezone=True), server_default=sa.func.now(), nullable=False
    )
    content = db.Column(db.TEXT())
    user_id = db.Column(db.UUID, db.ForeignKey("user_profiles.uid"))
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"))
