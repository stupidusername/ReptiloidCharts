from config import Config
from createapp import create_app, db
from datetime import datetime
import json
import logging
from logging.handlers import RotatingFileHandler
from models.entity import Entity
from models.status import Status
import re
from sqlalchemy import or_
import time
import twitter

# Create a rotating log for errors.
logger = logging.getLogger()
logger.setLevel(logging.ERROR)
handler = RotatingFileHandler('logs/search.log', maxBytes=65536, backupCount=5)
logger.addHandler(handler)
# Also send errors to stderr.
logger.addHandler(logging.lastResort)

# Create the app.
app = create_app()
# Push an application context to bind the SQLAlchemy object to your
# application.
app.app_context().push()

# Get app config.
config = Config()

# Twitter API.
twitter_api = twitter.Api(
    consumer_key=config.get_twitter_consumer_key(),
    consumer_secret=config.get_twitter_consumer_secret(),
    access_token_key=config.get_twitter_access_token_key(),
    access_token_secret=config.get_twitter_access_token_secret(),
    sleep_on_rate_limit=True
)


def _get_tweets(entity: Entity):
    """
    Get and save tweets metioning an entity.

    Twitter standard API only returns tweets that are less than a week old.

    :param Entity entity: Entity model instance.
    """
    # Build term query.
    term = '@{}'.format(entity.screen_name)
    if entity.name:
        term += ' OR "{}"'.format(entity.name)
    # This query param is used for pagination.
    max_id = None
    # Retrieve results until there are no more available.
    while True:
        # Make the API request.
        result = twitter_api.GetSearch(
            term=term,
            count=100,
            max_id=max_id,
            return_json=True)
        # Save tweets.
        for status in result.get('statuses', []):
            # Search for the same tweet in the DB.
            model = \
                Status.query.filter(Status.status_id == status['id']).first()
            # Create a new one if it was not found.
            if not model:
                model = Status()
            # Set tweet properties.
            model.entity_id = entity.id
            model.user_screen_name = status['user']['screen_name']
            model.status_id = status['id']
            model.create_datetime = datetime.strptime(
                status['created_at'],
                '%a %b %d %H:%M:%S %z %Y'
            )
            model.status = status['text']
            model.reply_count = 0  # Reply count can't be read from the API.
            model.retweet_count = status['retweet_count']
            model.favorite_count = status['favorite_count']
            # Save only if it's a new record.
            if not model.id:
                db.session.add(model)
            # Commit changes.
            db.session.commit()
        # next_results is an URL query.
        next_results = \
            result.get('search_metadata', {}).get('next_results', None)
        if not next_results:
            # No more results. Exit the loop.
            break
        else:
            # Get max_id from next_results.
            max_id = int(re.search('\?max_id=(\d+)', next_results).group(1))


def _search():
    """
    Search the tweets that mention any of the loaded entities.
    """
    # Get entities.
    entities = Entity.query.\
        filter(or_(Entity.deleted == None, Entity.deleted == False)).\
        filter(Entity.track == True).all()
    # Get and save tweets.
    for entity in entities:
        _get_tweets(entity)


# Execute search.
while True:
    try:
        _search()
    except Exception as e:
        logger.exception('Exception raised during search.')
    # Execute again in one hour.
    time.sleep(3600)
