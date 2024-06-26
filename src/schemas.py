from src.models.sports import Sport
from src.models.athletes import Team, TeamMember, TeamSchedule, TrainingTasks, TrainingTasksProgress
from src.models.social import Comment, Post
from src.models.user_profile import Role, User
from vars.enums import OrderDirection
from src.deps.ma import ma
from apifairy import FileField
from marshmallow import post_dump, post_load, validate, validates_schema, ValidationError
from datetime import datetime

paginated_schema_cache: dict = {}


class EmptySchema(ma.Schema):
    pass


class HTTPRequestSchema(ma.Schema):
    """
    Schema for http request response

    Details:
        code = Status Code
        message = Status Message
        description = API Response Description
    """

    code = ma.Int()
    message = ma.Str()
    description = ma.Str()


class OKRequestSchema(HTTPRequestSchema):
    """
    Schema for OK Request

    Details:
        code = Status Code
        message = Status Message
        description = API Response Description
    """

    code = ma.Int(missing=200, default=200)
    message = ma.Str(missing="OK", default="OK")
    description = ma.Str(missing="Request successful", default="Request succeessful")


class SignupSchema(ma.Schema):
    """
    Schema for Signup

    Details:
        email = Email
        password = Password
    """

    email = ma.Str(required=True)
    password = ma.Str(required=True)


class UploadMultipleDocumentsSchema(ma.Schema):
    document = ma.List(FileField(), required=True)


class UploadDocumentSchema(ma.Schema):
    document = FileField(required=True)


class RoleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Role


class ProfileSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User

    active_role = ma.Nested(RoleSchema)


class PostSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Post

    user_id = ma.UUID()


class CommentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Comment
    user_id = ma.UUID()
    user = ma.Nested(ProfileSchema, dump_only=True)


class SocialPostSchema(PostSchema):
    comments = ma.Nested(CommentSchema, many=True)
    post_date_string_repr = ma.String()
    user = ma.Nested(ProfileSchema)
    comments_count = ma.Integer()

    @post_dump
    def add_comments_count(self, data, **kwargs):
        data["comments_count"] = len(data["comments"])

        # difference of time today and created_at
        data["post_date_string_repr"] = self.get_date_string_repr(data["created_at"])
        return data

    def get_date_string_repr(self, created_at):
        created_at = datetime.strptime(str(created_at), "%Y-%m-%dT%H:%M:%S.%f%z")
        today = datetime.now(created_at.tzinfo)
        diff = today - created_at
        if diff.days > 4:
            return created_at.strftime("%b %d, %Y")
        elif diff.days > 0:
            return f"{diff.days} days ago"
        elif diff.seconds > 3600:
            return f"{int(diff.seconds/3600)} hours ago"
        elif diff.seconds > 60:
            return f"{int(diff.seconds/60)} minutes ago"
        else:
            return f"{diff.seconds} seconds ago"


class TeamSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Team

    # sport_id = ma.Integer(load_only=True)
    user_id = ma.UUID(load_only=True)


class SportSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Sport


class TaskProgressSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TrainingTasksProgress

    user_id = ma.UUID()


class TeamMemberSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TeamMember

    user_id = ma.UUID(load_only=True)
    created_at = ma.DateTime(data_key="joined_at")
    user = ma.Nested(ProfileSchema, dump_only=True)

    tasks = ma.Nested(TaskProgressSchema, many=True)

    task_count = ma.Integer(dump_only=True)

    @post_dump
    def add_task_count(self, data, **kwargs):
        data["task_count"] = len(data["tasks"])
        return data

    @post_dump(pass_many=True)
    def exclude_is_pending(self, data, many, **kwargs):
        print(data)
        print(many)
        # if not data.get("pending"):
        return_data = []
        for d in data:
            if not d.get("pending"):
                return_data.append(d)
        return return_data


class TeamMemberSchemaNormal(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TeamMember

    user_id = ma.UUID(load_only=True)
    created_at = ma.DateTime(data_key="joined_at")
    user = ma.Nested(ProfileSchema, dump_only=True)



class TeamsSchema(TeamSchema):
    team_members = ma.Nested(TeamMemberSchema, many=True)
    sport = ma.Nested(SportSchema)
    team_member_count = ma.Integer(dump_only=True)

    @post_dump
    def add_team_member_count(self, data, **kwargs):
        data["team_member_count"] = len(data["team_members"])
        return data


class TasksSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TrainingTasks


class WholeTasksSchema(TasksSchema):
    progress = ma.Nested(TaskProgressSchema(only=(['user_id','task_status'])), many=True)


class ScheduleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TeamSchedule


class ScheduleSpecificSchema(ma.Schema):
    description = ma.Str()
    location = ma.Str()
    title = ma.Str()
    opponent = ma.Str()
    date = ma.Date()
    user_id = ma.UUID()


class StatisticsSchema(ma.Schema):
    id = ma.Integer()
    stats_key = ma.Str()
    stats_value = ma.Str()
    user_id = ma.UUID()


class StringPaginationSchema(ma.Schema):
    class Meta:
        ordered = True

    limit = ma.Integer()
    offset = ma.Integer()
    order_by = ma.String(load_only=True)
    order_direction = ma.String(
        validate=validate.OneOf(OrderDirection.list()),
        load_only=True,
        missing=OrderDirection.DESC.value,
    )
    count = ma.Integer(dump_only=True)
    total = ma.Integer(dump_only=True)

    @validates_schema
    def validate_schema(self, data, **kwargs):
        if data.get("offset") is not None and data.get("after") is not None:
            raise ValidationError("Cannot specify both offset and after")


def PaginatedCollection(schema, pagination_schema=StringPaginationSchema):
    if schema in paginated_schema_cache:
        return paginated_schema_cache[schema]

    class PaginatedSchema(ma.Schema):
        class Meta:
            ordered = True

        pagination = ma.Nested(pagination_schema)
        data = ma.Nested(schema, many=True)

    PaginatedSchema.__name__ = "Paginated{}".format(schema.__class__.__name__)
    paginated_schema_cache[schema] = PaginatedSchema
    return PaginatedSchema
