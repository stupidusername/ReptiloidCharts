from config import Config
from createapp import create_app
import logging
from logging.handlers import RotatingFileHandler
from models.entity import Entity
import time
import twitter

# Create a rotating log.
logger = logging.getLogger()
logger.setLevel(logging.ERROR)
handler = RotatingFileHandler('logs/search.log', maxBytes=65536, backupCount=5)
logger.addHandler(handler)

# Create an app context so models can be used.
app = create_app()
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


def _search():
    """
    Search the tweets that mention any of the loaded entities.
    """
    entities = Entity.query.all()


# Execute search.
while True:
    try:
        _search()
    except Exception:
        logger.exception('Exception raised during search.')
    # Execute again in one hour.
    time.sleep(3600)
