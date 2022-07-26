import psycopg

from .mvars import PG_SQL_IP


def create_user(name):
    conn = get_root_connection()
    conn.autocommit=True
    db_name = name+'db'

    with conn:
        with conn.cursor() as cursor:
            cursor.execute('CREATE DATABASE {};'.format(db_name))
            cursor.execute(
                "CREATE USER {0} WITH ENCRYPTED PASSWORD 'abc';".format(name))
            cursor.execute('GRANT ALL PRIVILEGES ON DATABASE {1} TO {0};'.format(
                name, db_name))

def get_connection(db_user, db_name, pwd='abc'):
    conn = psycopg.connect(user=db_user, database=db_name, password=pwd,
                            host=PG_SQL_IP)
    return conn


def get_root_connection():
    conn = psycopg.connect(user="postgres", password="my-secret-pw",
                            host=PG_SQL_IP)
    return conn
