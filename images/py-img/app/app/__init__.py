import os
import pymysql.cursors
from flask import Flask, render_template, jsonify


def get_connection():
    connection = pymysql.connect(host='mysql-db',
                                user=os.environ.get('DB_LOGIN'),
                                password=os.environ.get('DB_PWD'),
                                database=os.environ.get('DB_NAME'),
                                charset='utf8mb4',
                                cursorclass=pymysql.cursors.DictCursor)
    return connection


def create_app():
    app = Flask(__name__)

    @app.route('/')
    def hello_world():

        # connection = get_connection()

        # with connection:
        #     with connection.cursor() as cursor:
        #         cursor.execute('SHOW DATABASES')
        #         rs = jsonify(cursor.fetchall())


        return render_template('index.html')

    return app
