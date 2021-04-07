import os, json
from flask import Blueprint, send_from_directory, current_app, make_response, render_template, jsonify

from . import users, list_dir

def get_blueprint():
    review = Blueprint('review_bp', __name__,
                       template_folder='templates',
                       static_folder='static')

    @review.route('/show_all', methods=['GET'])
    def show_all():
        conn = users.get_connection()
        with conn:
            with conn.cursor() as cursor:
                cursor.execute('select identity,nickname,db_vendor,lang from PROJECT inner join USER on identity=ref_identity;')
                sql_rs = cursor.fetchall()
                    

        return render_template('viewall.html', vlist=json.dumps(sql_rs))

    @review.route('/review_project/<string:identity>', methods=['GET'])
    def review_project(identity):

        conn = users.get_connection()
        with conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    'select lang from db_jeeves.PROJECT where ref_identity = %s', identity)
                sql_rs = cursor.fetchone()

                cursor.execute(
                    'select nickname from db_jeeves.USER where identity = %s', identity)
                reviewed_user_rs = cursor.fetchone()

        lang, pth = sql_rs and sql_rs['lang'], os.path.join(
            'users', identity, 'app')

        if not lang:
            return '<h1>Not Found<h1><h2>No project created for this user</h2>'

        has_diagram = os.path.exists(os.path.join(
            os.getcwd(), 'users', identity, identity+".pdf"))

        return render_template('index.html',
                               has_diagram=has_diagram,
                               reviewed_user=reviewed_user_rs['nickname'],
                               read_only='true',
                               force_update='false',
                               script_lang=lang,
                               app_path=list_dir.map_lang_dir(lang, pth))


    @review.route('/view_diagram/<string:identity>', methods=['GET'])
    def view_diagram(identity):

        pth = os.path.join(os.getcwd(), 'users', identity)

        response = make_response(send_from_directory(pth, identity+".pdf"))

        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        
        return response

    return review