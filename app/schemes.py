import os
import pymysql.cursors
from pymysql.constants import CLIENT
from flask import Blueprint, request, render_template, jsonify
from flask_login import current_user

from . import schemes_pg
from .mvars import MY_SQL_IP


def create_user(name):
    dname = '{}db'.format(name)
    schema_sql = '''
    START TRANSACTION;
    CREATE USER '{0}' IDENTIFIED WITH mysql_native_password BY 'abc';
    CREATE DATABASE `{1}`;
    GRANT ALL PRIVILEGES ON `{1}` . * TO '{0}';
    FLUSH PRIVILEGES;
    COMMIT;
    '''.format(name, dname)

    conn = get_root_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(schema_sql)
            conn.commit()

def get_connection(db_user, db_name, pwd='abc'):
    connection = pymysql.connect(host=MY_SQL_IP,
                                 user=db_user,
                                 db=db_name,
                                 password=pwd,
                                 charset='utf8mb4',
                                 client_flag=CLIENT.MULTI_STATEMENTS,
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection


def get_root_connection():
    connection = pymysql.connect(host=MY_SQL_IP,
                                 user='root',
                                 password='my-secret-pw',
                                 charset='utf8mb4',
                                 client_flag=CLIENT.MULTI_STATEMENTS,
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection

def get_test_root_connection():
    connection = pymysql.connect(host=MY_SQL_IP,
                                 user='root',
                                 database='test',
                                 password='my-secret-pw',
                                 charset='utf8mb4',
                                 client_flag=CLIENT.MULTI_STATEMENTS,
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection


def get_blueprint():
    schemes_bp = Blueprint('schemas_bp', __name__,
                           template_folder='templates',
                           static_folder='static')

    @schemes_bp.route('/edit_sql')
    def edit_sql():
        return render_template('sql_test.html')

    @schemes_bp.route('/run_sql', methods=['POST'])
    def run_sql():

        if request and request.json.get('sql'):

            identity = current_user.identity
            vendor = current_user.vendor
            dname = '{}db'.format(identity)

            if vendor == 'mysql':
                connection = get_connection(identity, dname)
                try:
                    with connection:
                        with connection.cursor() as cursor:
                            cursor.execute(request.json['sql'])
                            sql_rs = cursor.fetchall()
                except Exception as e:
                    return str(e), 400
            else:

                connection = schemes_pg.get_connection(identity, dname)
                try:
                    with connection:
                        with connection.cursor() as cursor:
                            cursor.execute(request.json['sql'])
                            connection.commit()
                            sql_rs = cursor.fetchall()
                except Exception as e:
                    return str(e), 400
            return jsonify(sql_rs)

        return '', 404

    return schemes_bp

