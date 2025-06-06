import logging
import os

import pymysql
import pymysqlpool
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=os.getenv(
    "LOG_LEVEL"), format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

LOKASI = os.getenv("LOKASI")


def get_connection_pool(autocommit: bool = False) -> pymysqlpool.Connection:
    """
    Return a connection from a pool of connections to the database.

    The connection pool is created with the following configuration:
    - size: 10
    - maxsize: 15
    - pre_create_num: 2
    - name: 'connection_pool'
    - autocommit: False
    - host: DB_HOST environment variable
    - port: int(DB_PORT environment variable)
    - user: DB_USER environment variable
    - password: DB_PASS environment variable
    - db: DB_NAME environment variable
    - charset: utf8mb4
    - cursorclass: pymysql.cursors.DictCursor

    Parameters:
    autocommit (bool): Whether to enable autocommit mode. Defaults to False.

    Returns:
    pymysqlpool.Connection: A connection to the database.
    """
    config = {
        'host': os.getenv('DB_HOST'),
        'port': int(os.getenv('DB_PORT')),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASS'),
        'database': os.getenv('DB_NAME'),
        'charset': 'utf8mb4',
        'cursorclass': pymysql.cursors.DictCursor
    }
    return pymysqlpool.ConnectionPool(
        size=10,
        maxsize=15,
        pre_create_num=2,
        name='connection_pool',
        autocommit=autocommit,
        **config
    ).get_connection()
