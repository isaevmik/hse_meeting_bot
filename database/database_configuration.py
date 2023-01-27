import psycopg2  # noqa
from decouple import config
from playhouse.postgres_ext import Model, PostgresqlExtDatabase  # noqa

db = PostgresqlExtDatabase(
    config("DB_NAME"),
    user=config("DB_USER"),
    password=config("DB_PASSWORD"),
    host=config("DB_HOST"),
    port=config("DB_PORT"),
    autorollback=True,
)
