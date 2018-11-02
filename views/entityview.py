
from flask import flash
from flask_admin import expose
from flask_admin.babel import gettext
from flask_admin.contrib.sqla import ModelView
from models.entity import Entity


class EntityView(ModelView):
    """
    Model view class for entity model.
    """

    # Remove columns from index view.
    column_exclude_list = ['deleted']

    # Remove fields from the create and edit forms.
    form_excluded_columns = ['deleted']

    def delete_model(self, model: Entity) -> bool:
        """
        Override. Set deleted to `True` instead of deleting the record.

        :returns: `True` if the operation succeeded.
        """
        try:
            self.on_model_delete(model)
            self.session.flush()
            model.deleted = True
            self.session.commit()
        except Exception as e:
            if not self.handle_view_exception(e):
                flash(
                    gettext(
                        'Failed to delete record. %(error)s',
                        error=str(e)
                    ),
                    'error'
                )
                log.exception('Failed to delete record.')
            self.session.rollback()
            return False
        else:
            self.after_model_delete(model)

        return True
