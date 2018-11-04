# ReptiloidCharts

![Reptiloid](reptiloid.jpg)


## Requirements

- Python >= 3.6 (Tested on 3.6.6).
- Pip packages listed on `requirements.txt`.
- A RDBMS supported by SQLAlchemy. See [SQLAlchemy 1.2 Documentation > Dialects](https://docs.sqlalchemy.org/en/latest/dialects/index.html).


## Installation

- Create a `config.ini`. Use `config-example.ini` as reference.
- Apply DB migrations: `$ alembic upgrade head`.


## Usage

Run the flask application defined in `app.py`. See [Flask deployment options](http://flask.pocoo.org/docs/1.0/deploying/).

Notes:
- Dates and times are displayed in UTC.
- Screen names should be entered without `@`.
- The app can only read tweets from the Twitter API that are less than 7 days old.
- The stats of a given tweet can only be tracked for the next 7 days following its creation. After that they will be frozen.
