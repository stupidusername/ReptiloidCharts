from api.getreactions import GetReactions
from createapp import create_app, db
from flask_admin import Admin
from flask_restful import Api
from models.entity import Entity
from views.entityview import EntityView
from views.homeview import HomeView

# Create the app.
app = create_app()
# Push an application context to bind the SQLAlchemy object to your
# application.
app.app_context().push()

# Initialize the admin interface.
admin = Admin(app, index_view=HomeView(url='/'))
admin.add_view(EntityView(Entity, db.session, name='Entities'))

# Create app API.
api = Api(app)
# Add API endpoints.
api.add_resource(
    GetReactions,
    '/api/get-reactions/<string:from_date>/<string:to_date>'
)
