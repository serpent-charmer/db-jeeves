import os
import pymysql.cursors


import psycopg2
import psycopg2.extras


def get_connection_mysql():
    connection = pymysql.connect(host='mysql-db',
                                 user=os.environ.get('DB_LOGIN'),
                                 password=os.environ.get('DB_PWD'),
                                 database=os.environ.get('DB_NAME'),
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection


def get_connection_pg():
    conn = psycopg2.connect(user=os.environ.get('DB_LOGIN'),
                            database=os.environ.get('DB_NAME'),
                            password=os.environ.get('DB_PWD'),
                            host='pgsql-db',
                            connection_factory=psycopg2.extras.RealDictConnection)
    return conn

# connection = get_connection()

    # with connection:
    #     with connection.cursor() as cursor:
    #         cursor.execute('select * from some_table')
    #         rs = cursor.fetchall()
