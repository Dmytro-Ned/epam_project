from flask import flash
from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, AnonymousUserMixin


class AdminMixin:  # mixin reduces code duplication

    create_modal = True
    edit_modal = True
    form_excluded_columns = ['uuid']

    def is_accessible(self):
        return current_user.is_superuser if not isinstance(current_user, AnonymousUserMixin) else False


class AlteredModelView(AdminMixin, ModelView):  # restricts access to the ORM models on the admin page
    pass

    def create_model(self, form):
        super().create_model(form=form)
        flash("Model created", category="success")

    def update_model(self, form, model):
        super().update_model(form=form, model=model)
        flash("Model altered", category="success")


class AlteredAdminIndexView(AdminMixin, AdminIndexView):  # restricts access to the admin page
    pass
