from flask import flash, url_for
from flask_admin.contrib.sqla import ModelView
from flask_admin import expose
from flask_admin.helpers import get_form_data
from flask_admin.babel import gettext
from flask import redirect
from markupsafe import Markup
from src.deps.admin import admin
from src.deps.db import db
from src.deps.supabase import supabase

from src.models.user_profile import User, AthleteProfile, CoachProfile
from src.models.social import Post, Comment
import uuid


class UserModelView(ModelView):
    can_create = False
    can_delete = False
    column_labels = dict(uid="User ID", active_role="Role")

    column_list = ["uid", "email", "requested_role", "active_role", "delete_user"]
    form_columns = ["active_role"]

    def _delete_user(view, context, model, name):
        delete_url = url_for(".delete_user")
        id = model.uid
        print(id)
        _html = f"""
            <form action="{delete_url}" method="post">
            <input type="hidden" name="uid" value="{id}">
            <button type="submit">Delete</button>
            </form>
        """

        return Markup(_html)

    column_formatters = {"delete_user": _delete_user}

    @expose("delete", methods=["POST"])
    def delete_user(self):
        return_url = url_for(".index_view")
        form = get_form_data()
        id = form.get("uid")
        if not form:
            flash(gettext("Could not get form from request."), "error")
            return redirect(return_url)

        try:
            supabase.auth.admin.delete_user(uuid.UUID(str(id)))
            flash(gettext("User deleted successfully."), "success")
        except Exception as ex:
            if not self.handle_view_exception(ex):
                raise

            flash(gettext("Failed to delete user", error=str(ex)), "error")

        return redirect(return_url)


class RoleModelView(ModelView):
    can_delete = False
    column_list = ["role_name"]
    form_columns = ["role_name"]


class CoachViewModel(ModelView):
    inline_models = (CoachProfile,)

    form_columns = ["active_role", "first_name", "middle_name", "last_name", "email", "gender", "phone_number", "birthdate", "coach_profile"]

    def get_query(self):
        return db.session.query(User).filter(User.role == 4)


class AthleteViewModel(ModelView):
    inline_models = (AthleteProfile,)

    form_columns = ["active_role", "first_name", "middle_name", "last_name", "email", "gender", "phone_number", "birthdate", "athlete_profile"]

    def get_query(self):
        return db.session.query(User).filter(User.role == 5)


class PostModelView(ModelView):
    column_list = ["title", "content", "user", "likes"]
    form_columns = ["title", "content", "user", "likes", "comments"]


class CommentModelView(ModelView):
    column_list = ["content", "user"]
    form_columns = ["content", "user", "post"]


admin.add_view(
    UserModelView(
        model=User,
        session=db.session,
        endpoint="users/edit",
        name="Edit Users Access",
        category="User Profiles",
    )
)

# admin.add_view(
#     RoleModelView(
#         model=Role,
#         session=db.session,
#         endpoint="roles/add",
#         name="Add Roles",
#         category="User Management",
#     )
# )


admin.add_view(
    CoachViewModel(
        model=User,
        session=db.session,
        name="Coach",
        endpoint="profiles/coach",
        category="User Profiles"
    )
)

admin.add_view(
    AthleteViewModel(
        model=User,
        session=db.session,
        name="Athlete",
        endpoint="profiles/athlete",
        category="User Profiles"
    )
)


admin.add_view(
    PostModelView(
        model=Post,
        session=db.session,
        name="Posts",
        endpoint="social/post",
        category="Social"
    )
)

admin.add_view(
    CommentModelView(
        model=Comment,
        session=db.session,
        name="Comments",
        endpoint="social/comment",
        category="Social"
    )
)
