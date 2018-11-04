from configparser import ConfigParser
from pathlib import Path


class Config(object):
    """
    This class provides access to the app configuration.
    """

    def __init__(self):
        self._config = ConfigParser()
        self._config.read(Path('config.ini'))

    def get_secret_key(self) -> str:
        """
        :returns: Secret key for cookies.
        """
        return self._config['DEFAULT']['secret_key']

    def get_sql_alchemy_url(self) -> str:
        """
        :returns: Database DSN.
        """
        return self._config['DEFAULT']['sqlalchemy.url']

    def get_twitter_consumer_key(self) -> str:
        """
        :returns: Twitter API consumer key.
        """
        return self._config['DEFAULT']['twitter_consumer_key']

    def get_twitter_consumer_secret(self) -> str:
        """
        :returns: Twitter API consumer secret.
        """
        return self._config['DEFAULT']['twitter_consumer_secret']

    def get_twitter_access_token_key(self) -> str:
        """
        :returns: Twitter API access token key.
        """
        return self._config['DEFAULT']['twitter_access_token_key']

    def get_twitter_access_token_secret(self) -> str:
        """
        :returns: Twitter API access token secret.
        """
        return self._config['DEFAULT']['twitter_access_token_secret']
