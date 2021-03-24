import os
import pymysql.cursors
from pymysql.constants import CLIENT
from flask import Blueprint, request, render_template, jsonify
from flask_login import current_user

from .dapi import MY_SQL_IP

def get_connection(db_user, db_name, pwd='abc'):
    connection = pymysql.connect(host=MY_SQL_IP,
                                 user=db_user,
                                 password=pwd,
                                 db=db_name,
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
            dname = 'database-{}'.format(identity)

            connection = get_connection(identity, dname)

            with connection:
                with connection.cursor() as cursor:

                    cursor.execute(request.json['sql'])
                    sql_rs = cursor.fetchall()

            return jsonify(sql_rs)

        return '', 404

    return schemes_bp

