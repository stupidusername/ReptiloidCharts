from config import Config
from createapp import create_app, db
import datetime
import json
import logging
from logging.handlers import RotatingFileHandler
from models.entity import Entity
from models.status import Status
import pytz
import re
from scrapers.twitterstatus import TwitterStatus
from sqlalchemy import or_
import time
import twitter
from typing import List

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


def _get_date_seven_days_ago() -> datetime.date:
    """
    Get date 7 days ago.

    :returns: A date object.
    """
    now = datetime.datetime.utcnow()
    seven_days_ago = now - datetime.timedelta(days=7)
    date_seven_days_ago = seven_days_ago.date()
    return date_seven_days_ago


def _get_entities() -> List[Entity]:
    """
    Get entity models that must be tracked.

    :returns: A list of entities.
    """
    entities = Entity.query.\
        filter(or_(Entity.deleted == None, Entity.deleted == False)).\
        filter(Entity.track == True).all()
    return entities


def _get_statuses(**kwargs) -> List[dict]:
    """
    Get statuses from Twitter API.

    :param **kwargs: Params passed to twitter.Api.GetSearch().
    :returns: A list of dictionaries representing the statuses. `return_json`
        is always set to `True` and `count` is always set to `100`. `max_id`
        will be igored because it is used internally.
    """
    statuses = []
    # Set count param.
    kwargs['count'] = 100
    # Set return_json param.
    kwargs['return_json'] = True
    # This query param is used for pagination.
    max_id = None
    # Retrieve results until there are no more available.
    while True:
        # Set max_id param.
        kwargs['max_id'] = max_id
        # Make the API request.
        result = twitter_api.GetSearch(**kwargs)
        # Add tweets to the reponse list.
        statuses.extend(result.get('statuses', []))
        # next_results is an URL query.
        next_results = \
            result.get('search_metadata', {}).get('next_results', None)
        if not next_results:
            # No more results. Exit the loop.
            break
        else:
            # Get max_id from next_results.
            max_id = int(re.search('\?max_id=(\d+)', next_results).group(1))
    return statuses


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
    # Get tweets.
    statuses = _get_statuses(term=term)
    # Save tweets.
    for status in statuses:
        # Get creation datetime of the tweet.
        create_datetime = datetime.datetime.strptime(
            status['created_at'],
            '%a %b %d %H:%M:%S %z %Y'
        ).astimezone(pytz.utc)
        # Filter out tweets that were not created this week.
        # For some reason the Twitter API returns some older tweets, even
        # though this contradicts the documentation.
        from_this_week = create_datetime.date() >= _get_date_seven_days_ago()
        # Filter out tweets that are not mentioning the entity. There might be
        # cases when the screen_name of the user that created the tweet
        # contains the name of the entity.
        text = status['text']
        # Match only if the screen_name or the name is in the text but leave
        # out the cases where the name is used inside an account reference.
        regex = '(?:\\b{}\\b)'.format(entity.screen_name)
        if entity.name:
            regex += '|(?:(?<!@)\\b_*{}_*\\b)'.format(re.escape(entity.name))
        is_mention = re.search(regex, text, re.IGNORECASE)
        if from_this_week and is_mention:
            # Search for the same tweet in the DB.
            model = Status.query.\
                filter(Status.status_id == status['id']).first()
            # Create a new one if it was not found.
            if not model:
                model = Status()
            # Set tweet properties.
            model.entity_id = entity.id
            model.user_screen_name = status['user']['screen_name']
            model.status_id = status['id']
            model.create_datetime = create_datetime
            model.status = text
            model.reply_count = 0  # Reply count is not in the results.
            model.retweet_count = status['retweet_count']
            model.favorite_count = status['favorite_count']
            # Save only if it's a new record.
            if not model.id:
                db.session.add(model)
            # Commit changes.
            db.session.commit()


def _count_replies():
    """
    Get and save reply count of each tweet.
    """
    # Count replies of each entity.
    entities = _get_entities()
    for entity in entities:
        # Get tweets from this week mentioning that entity.
        statuses = Status.query.\
            filter(Status.entity_id == entity.id).\
            filter(Status.create_datetime >= _get_date_seven_days_ago()).all()
        # Scrap the reply count.
        for status in statuses:
            twitter_status = TwitterStatus(status.status_id)
            reply_count = twitter_status.get_reply_count()
            # Save the result.
            status.reply_count = reply_count
            db.session.commit()


def _search():
    """
    Search the tweets that mention any of the loaded entities.
    """
    # Get entities.
    entities = _get_entities()
    # Get and save tweets and their reaction count.
    for entity in entities:
        _get_tweets(entity)
        _count_replies()


# Execute search.
while True:
    try:
        _search()
    except Exception as e:
        logger.exception('Exception raised during search.')
    # Execute again in one hour.
    time.sleep(3600)
