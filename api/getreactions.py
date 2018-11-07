from flask_restful import Resource


class GetReactions(Resource):
    """
    Flask-RESTful resource.
    """

    def get(self, from_date: str, to_date: str) -> dict:
        """
        Get total reaction counts of the entities organized by date.

        Only results that are between `from_date` and `to_date` are returned.

        :param str from_date: A date with the format `YYYY-MM-DD`. Return
            results created after this date (inclusive).
        :param str to_date: A date with the format `YYYY-MM-DD`. Return
            results created before this date (non-inclusive).
        :returns: A dictionary containing the entities an their reaction counts
            organized by date. See the documentation of the
            `/api/get-reactions` endpoint in the app README.
        """
        return {'result': ':D'}
