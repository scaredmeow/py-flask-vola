from flask import Blueprint, abort
from src.models.social import Post
from src.decorators import paginated_response
from src.schemas import OKRequestSchema, SocialPostSchema, PostSchema, UploadDocumentSchema
from apifairy import body, response

app = Blueprint("Social", __name__)


@app.route("/posts", methods=["GET"])
@paginated_response(SocialPostSchema)
def get_all_posts(data: dict):
    return Post.query


@app.route("/posts/new", methods=["POST"])
@body(UploadDocumentSchema, location="form", media_type="multipart/form-data")
@response(OKRequestSchema)
def create_post(data: dict, id: int):
    """Create new post"""
    document = data.get("document")

    try:
        hackathon = Post.query.get_or_404(id)
        Post.insert_image(document)
    except Exception as e:
        abort(400, str(e))

