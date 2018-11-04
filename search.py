from config import Config
import logging
from logging.handlers import RotatingFileHandler
import twitter

# Create a rotating log.
logger = logging.getLogger()
logger.setLevel(logging.ERROR)
handler = RotatingFileHandler('logs/search.log', maxBytes=65536, backupCount=5)
logger.addHandler(handler)

# Get app config.
config = Config()

# Twitter API.
twitter_api = twitter.Api(
    consumer_key=config.get_twitter_consumer_key(),
    consumer_secret=config.get_twitter_consumer_secret(),
    access_token_key=config.get_twitter_access_token_key(),
    access_token_secret=config.get_twitter_access_token_secret()
)
