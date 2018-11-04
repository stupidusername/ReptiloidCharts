from config import Config
import twitter

# Get app config.
config = Config()

# Twitter API.
twitter_api = twitter.Api(
    consumer_key=config.get_twitter_consumer_key(),
    consumer_secret=config.get_twitter_consumer_secret(),
    access_token_key=config.get_twitter_access_token_key(),
    access_token_secret=config.get_twitter_access_token_secret()
)
