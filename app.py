from config import Config
from flask import Flask
from flask_admin import Admin
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

# Create and configure app.
app = Flask(__name__)
config = Config()
app.config['SECRET_KEY'] = config.get_secret_key()
app.config['SQLALCHEMY_DATABASE_URI'] = config.get_sql_alchemy_url()

# Create app components.
api = Api(app)
# Variable db must be declared before the rest of the imported classes use it.
db = SQLAlchemy(app)

# Import models.
from models.entity import Entity

# Import views.
from views.entityview import EntityView
from views.homeview import HomeView

# Initialize the admin interface.
admin = Admin(app, index_view=HomeView(url='/'))
admin.add_view(EntityView(Entity, db.session, name='Entities'))

# Import api resources.

# Add API endpoints.
