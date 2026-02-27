import psycopg2
from contextlib import contextmanager
from .config import DataBaseConfig
@contextmanager
def create_connection(config: DataBaseConfig):
    connection = None
    try:
        connection = psycopg2.connect(**config.get_connection_params())
        yield connection
    except psycopg2.OperationalError as e:
        if connection:
            connection.rollback()
        raise
    finally:
        if connection:
            connection.close()