# ReptiloidCharts

![Reptiloid](reptiloid.jpg)


## Requirements

- Python >= 3.6 (Tested on 3.6.6).
- Pip packages listed on `requirements.txt`.
- A RDBMS supported by SQLAlchemy. See [SQLAlchemy 1.2 Documentation > Dialects](https://docs.sqlalchemy.org/en/latest/dialects/index.html).
- A Twitter app. You can create one [here](https://apps.twitter.com/).


## Installation

- Create a `config.ini`. Use `config-example.ini` as reference.
- Apply DB migrations: `$ alembic upgrade head`.


## Usage

- Run the flask application defined in `app.py`. See [Flask deployment options](http://flask.pocoo.org/docs/1.0/deploying/).
- Run `search.py` in the background. This scripts searches the tweets using the Twitter API.
Only one instance should be executing at a time. In the unlikely case that it fails, you should restart it.


## Notes

- Dates and times are displayed in UTC.
- Screen names should be entered without `@`.
- Only entities that have its `Track` option enabled will we tracked.
- The app can only read tweets from the Twitter API that are less than 7 days old.
- The stats of a given tweet can only be tracked for the next 7 days following its creation. After that they will be frozen.


## API endpoints

- `/api/get-reactions/<from_date>/<to_date>`

  Get a list of the loaded entities with its reactions by day.
  Keep in mind that the reactions from a given date corresponds to the summatory of the reactions of the tweets that were created that day.

  - Params:

    - `from_date`: Return reactions of tweets that where created after this date (inclusive). Format: `YYYY-MM-DD`.
    - `to_date`: Return reactions of tweets that where created before this date (inclusive). Format: `YYYY-MM-DD`.

  - Response example:

    ```
    [
      {
        "entity": {
          "id": 1,
          "screen_name": "john_doe",
          "name": "John Doe",
          "track": true
        },
        "reactions": [
          {
            "date": "2018-11-05",
            "reaction_count": 10
          },
          {
            "date": "2018-11-06",
            "reaction_count": 5
          }
        ]
      },
      {
        "entity": {
          "id": 2,
          "screen_name": "jane_doe",
          "name": "Jane Doe",
          "track": false
        },
        "reactions": [
          {
            "date": "2018-11-05",
            "reaction_count": 7
          },
          {
            "date": "2018-11-06",
            "reaction_count": 13
          }
        ]
      }
    ]
    ```
