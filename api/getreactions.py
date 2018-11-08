from createapp import db
from datetime import datetime
from flask_restful import Resource
from models.entity import Entity
from models.status import Status
from sqlalchemy.sql import func


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
        # Convert string dates to date objects.
        from_converted = datetime.strptime(from_date, '%Y-%m-%d').date()
        to_converted = datetime.strptime(to_date, '%Y-%m-%d').date()
        # Get results from the DB.
        results = db.session.query(
            Entity,
            func.date(Status.create_datetime).label('date'),
            func.count(Status.id).label('mention_count'),
            (
                func.sum(Status.reply_count) +
                func.sum(Status.retweet_count) +
                func.sum(Status.favorite_count)
            ).label('reaction_count')
        ).join(
            Status
        ).filter(
            Status.create_datetime >= from_converted,
            Status.create_datetime < to_converted
        ).order_by(
            func.date(Status.create_datetime).asc()
        ).group_by(
            Status.entity_id,
            func.date(Status.create_datetime)
        ).all()
        # Index the results by entity id.
        indexed_results = {}
        for result in results:
            entity_id = result[0].id
            if entity_id in indexed_results:
                indexed_results[entity_id].append(result)
            else:
                indexed_results[entity_id] = [result]
        # Create the response.
        response = []
        for result_list in indexed_results.values():
            reactions = []
            for result in result_list:
                reactions.append({
                    'date': result[1],
                    'mention_count': result[2],
                    'reaction_count': result[3]
                })
            entity = result_list[0][0]
            response.append({
                'entity': {
                    'id': entity.id,
                    'screen_name': entity.screen_name,
                    'name': entity.name,
                    'track': entity.track
                },
                'reactions': reactions
            })
        return response
