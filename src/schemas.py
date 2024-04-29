from src.models.user_profile import Role, User
from vars.enums import OrderDirection
from src.deps.ma import ma
from apifairy import FileField
from marshmallow import validate, validates_schema, ValidationError

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
