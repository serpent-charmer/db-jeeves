from flask import Flask, render_template, jsonify





def create_app():
    app = Flask(__name__)

    @app.route('/')
    def hello_world():

        

        return render_template('index.html')

    return app
