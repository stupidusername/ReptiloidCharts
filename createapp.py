from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

# Create the global SQLAlchemy object.
db = SQLAlchemy()


def create_app() -> Flask:
    """
    Create and configure an app.

    :returns: A Flask app.
    """
    config = Config()
    app = Flask('app')
    app.config['SECRET_KEY'] = config.get_secret_key()
    app.config['SQLALCHEMY_DATABASE_URI'] = config.get_sql_alchemy_url()
    db.init_app(app)
    return app
