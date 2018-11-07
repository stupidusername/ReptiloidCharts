from lxml import html
from lxml.etree import tostring
import requests
from requests import Session
from scrapers.twitter import Twitter
from typing import Optional


class TwitterStatus(Twitter):
    """
    This class represents a twitter status and it uses scraping to get its
    information.

    :param int id: Tweet id.
    :param None|Session session: A request session can be passed to the
        constructor. This can be useful to make the requests as a logged in
        user.
    """

    def __init__(self, id: int, session: Optional[Session] = None):
        # Session used to keep cookies.
        self._session = session if session else requests.Session()
        # Default attribute values.
        self._id = id
        self._status = None
        self._tree = None
        # Status URL.
        self._status_url = self.BASE_URL + '/statuses/' + str(self._id)
        # Make the request.
        headers = {}
        # Send referer header if the request is from a logged in session.
        if session:
            # If this header is not sent, the user is redirected to an empty
            # page that contains a javascript redirect to the requested page.
            headers = {'Referer': self.AFTER_LOGIN_REFERER}
        response = self.make_request(
            self._session,
            self._status_url,
            'get',
            headers=headers
        )
        # Create the element tree.
        self._tree = html.fromstring(response.content)
        # Populate status.
        elements = self._tree.find_class('TweetTextSize--jumbo')
        if elements:
            self._status = elements[0].text_content()

    def get_status(self) -> Optional[str]:
        """
        Get the status message.

        :returns: The status message or None if the status could not be
            retrieved.
        """
        return self._status

    def get_reply_count(self) -> int:
        """
        Get the reply count of the status.

        :returns: The reply count.
        """
        reply_count = None
        # Find reply count.
        elements = self._tree.xpath(
            "//span[contains(@class, 'ProfileTweet-action--reply')]"
            "/span[contains(@class, 'ProfileTweet-actionCount')]"
        )
        if elements:
            reply_count = elements[0].get('data-tweet-stat-count')
        # Check that the reply count was found.
        if reply_count is None:
            raise TwitterScrapingException('Reply count not found.')
        return reply_count
