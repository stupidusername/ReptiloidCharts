from createapp import db


class Status(db.Model):
    """
    Status model.
    """

    id = db.Column('id', db.Integer, primary_key=True)
    entity_id = db.Column(
        'entity_id',
        db.Integer,
        db.ForeignKey('entity.id'),
        nullable=False
    )
    user_screen_name = \
        db.Column('user_screen_name', db.String(), nullable=False)
    status_id = db.Column('status_id', db.Integer, nullable=False, unique=True)
    create_datetime = \
        db.Column('create_datetime', db.DateTime(), nullable=False)
    status = db.Column('status', db.Text(), nullable=False)
    reply_count = db.Column('reply_count', db.Integer, nullable=False)
    retweet_count = db.Column('retweet_count', db.Integer, nullable=False)
    favorite_count = db.Column('favorite_count', db.Integer, nullable=False)
