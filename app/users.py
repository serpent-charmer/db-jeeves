import pymysql.cursors
from pymysql.constants import CLIENT


def get_connection():
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='test',
                                 database='db_jeeves',
                                 charset='utf8mb4',
                                 client_flag=CLIENT.MULTI_STATEMENTS,
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection
