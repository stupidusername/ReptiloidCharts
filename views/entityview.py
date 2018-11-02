from flask_admin import expose
from flask_admin.contrib.sqla import ModelView


class EntityView(ModelView):
    """
    Model view class for entity model.
    """

    # Remove columns from index view.
    column_exclude_list = ['deleted']

    # Remove fields from the create and edit forms.
    form_excluded_columns = ['deleted']
