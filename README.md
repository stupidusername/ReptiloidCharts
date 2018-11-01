# ReptiloidCharts

![Reptiloid](reptiloid.jpg)


## Requirements

- Python >= 3.6 (Tested on 3.6.6).
- Pip packages listed on `requirements.txt`.
- A RDBMS supported by SQLAlchemy. See [SQLAlchemy 1.2 Documentation > Dialects](https://docs.sqlalchemy.org/en/latest/dialects/index.html).


## Installation

- Create a `config.ini`. Change the database DSN and the secret key used for cookies. Use `config-example.ini` as reference.
- Apply DB migrations: `$ alembic upgrade head`.


## Usage

Run the flask application defined in `app.py`. See [Flask deployment options](http://flask.pocoo.org/docs/1.0/deploying/).

Note: Dates and times are displayed in UTC.
