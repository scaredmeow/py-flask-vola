from tempfile import NamedTemporaryFile
import uuid
from src.deps.db import db, QueryModel
from src.deps.supabase import supabase
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

    def insert_image(self, document):
        document_uuid: str = str(uuid.uuid4())
        document_ext: str = document.filename.split(".")[-1]
        document_name: str = f"{document_uuid}.{document_ext}"

        self.image = document_name
        self.update_record()

        temp = NamedTemporaryFile(delete=False)
        document.save(temp.name)

        with open(temp.name, "rb") as f:
            supabase.storage.from_("static").upload(
                file=f,
                path=self.upload,
                file_options={"content-type": "image/jpeg"}
            )


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
