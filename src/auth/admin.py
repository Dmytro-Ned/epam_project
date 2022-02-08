"""
A module which manages ADMIN panel functionality.
"""


from flask import flash
from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, AnonymousUserMixin


class AdminMixin:  # mixin reduces code duplication
    """
    A mixin class with common functionality
    for admin homepage and model representation pages.

    methods:
     - is_accessible
    """

    create_modal = True  # uses modals stead of typical forms
    edit_modal = True
    form_excluded_columns = ['uuid']  # uuid will not be accessible from the panel

    def is_accessible(self):
        """
        Defines if the admin panel and its functionality
        is accessible for the user of the current session.

        :return bool: an indicator of accessibility
        """
        return current_user.is_superuser if \
            not isinstance(current_user, AnonymousUserMixin) else False


class AlteredModelView(AdminMixin, ModelView):  # restricts access to ORM models on the admin page
    """
    A class which manages access to models
    from admin panel and their interface.

    methods:
      - create_model
      - update_model
    """

    def create_model(self, form):
        """
        Extends "create_model" method of the ModelView class.
        Governs the creation of a new DB object
        from the admin panel.

        :param form: the form for creation of an object
        """
        super().create_model(form=form)
        flash("Model created", category="success")

    def update_model(self, form, model):
        """
        Extends "create_model" method of the ModelView class.
        Governs the alteration of an existing DB object
        from the admin panel.

        :param FlaskForm form: the form for alteration of an object
        :param SQLAlchemy().Model model: the model of an object to be altered
        """
        super().update_model(form=form, model=model)
        flash("Model altered", category="success")


class AlteredAdminIndexView(AdminMixin, AdminIndexView):  # restricts access to the admin page
    """
    A class which manages main admin panel page
    and its accessibility.
    """
