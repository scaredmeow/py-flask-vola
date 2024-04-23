from functools import wraps
import copy

from flask import abort
from apifairy import arguments, response
import sqlalchemy as sqla
from src.deps.db import db
from src.schemas import StringPaginationSchema, PaginatedCollection


def paginated_response(
    schema,
    max_limit: int = 25,
    order_by_default: str = None,
    limit_keys: dict = None,
    filter_keys: list = None,
    pagination_schema=StringPaginationSchema,
):
    def inner(f):
        @wraps(f)
        def paginate(*args, **kwargs):
            args = list(args)
            pagination = args.pop(-1)
            query_args = {}
            filter_args = []
            filter_values = []
            for arg in args:
                query_args.update(arg)

            search_val = {}

            if filter_keys:
                search_val = copy.deepcopy(query_args)
            args = copy.deepcopy(query_args)

            if filter_keys and query_args:
                tmp = 1
                for key in list(query_args.keys()):
                    if key not in filter_keys:
                        search_val.pop(key)
                    if limit_keys and key in list(limit_keys.keys()):
                        filter_args.append(limit_keys[key] + ":query_args" + str(tmp))
                        filter_values.append(query_args[key])
                        tmp += 1

            args = [args]

            order_by = pagination.get("order_by") or order_by_default
            order_direction = pagination.get("order_direction", "desc")
            select_query = f(*args, **kwargs)

            if search_val:
                select_query = select_query.filter_by(**search_val)

            if filter_args:
                select_query = select_query.filter(
                    *[sqla.text(arg) for arg in filter_args]
                ).params(
                    {
                        "query_args" + str(index + 1): arg
                        for index, arg in enumerate(filter_values)
                    }
                )

            if order_by is not None:
                o = order_by + " desc" if order_direction == "desc" else order_by
                select_query = select_query.order_by(sqla.text(o))

            count = db.session.scalar(
                sqla.select(sqla.func.count()).select_from(select_query.subquery())
            )

            limit = pagination.get("limit", max_limit)
            offset = pagination.get("offset")

            if limit > max_limit:
                limit = max_limit
            else:
                if offset is None:
                    offset = 0
                if offset < 0 or (count > 0 and offset >= count) or limit <= 0:
                    abort(400, "Invalid offset value")

            query = select_query.limit(limit).offset(offset)

            data = db.session.scalars(query).all()

            return {
                "data": data,
                "pagination": {
                    "offset": offset,
                    "limit": limit,
                    "count": len(data),
                    "total": count,
                },
            }

        # wrap with APIFairy's arguments and response decorators
        return arguments(pagination_schema)(
            response(PaginatedCollection(schema, pagination_schema=pagination_schema))(
                paginate
            )
        )

    return inner
