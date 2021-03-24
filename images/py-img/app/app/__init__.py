import os
import pymysql.cursors
from flask import Flask, render_template



connection = pymysql.connect(host='mysql-db',
                             user=os.environ.get('DB_LOGIN'),
                             password=os.environ.get('DB_PWD'),
                             database=os.environ.get('DB_NAME'),
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


def create_app():
    app = Flask(__name__)

    @app.route('/')
    def hello_world():

        with connection:
            with connection.cursor() as cursor:
                cursor.execute('SHOW DATABASES')
                print(cursor.fetchall())


        return render_template('index.html')

    return app
