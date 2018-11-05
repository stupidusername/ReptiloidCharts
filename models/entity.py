from createapp import db


class Entity(db.Model):
    """
    Entity model.
    """

    id = db.Column('id', db.Integer, primary_key=True)
    screen_name = db.Column('screen_name', db.String(), nullable=False)
    name = db.Column('name', db.String())
    track = db.Column('track', db.Boolean)
    deleted = db.Column('deleted', db.Boolean)
