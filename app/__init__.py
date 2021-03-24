import os

from flask import Flask, session, render_template, jsonify, request, redirect, session, current_app
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from distutils.dir_util import remove_tree
from . import dapi, list_dir, langs, users


def get_app():
    app = Flask(__name__, static_url_path='/static')
    app.secret_key = 'xxx_secret_xxx'

    with app.app_context():
        from . import schemes
        from . import auth
        app.register_blueprint(schemes.get_blueprint())
        app.register_blueprint(auth.get_blueprint())

    @app.route('/', methods=['GET'])
    @login_required
    def main():
        return render_template('main.html')

    @app.route('/sync_changes', methods=['POST'])
    def sync_changes():
        if not request and not request.json:
            return '', 404
        for entr in request.json.items():
            dpath, changed = entr
            print(dpath, changed)
            with open(dpath, 'w+') as f:
                f.write(changed)
        return jsonify(['ok'])

    @app.route('/restart_instance', methods=['POST'])
    def restart_instance():
        if request and request.json.get('user'):
            nm = request.json['user']
            container = dapi.build_custom_img(os.path.join('users', nm), nm)
            port = dapi.get_container_port(container)
            return jsonify({'port': port})
        return '', 404

    @app.route('/view_project')
    def view_your_project():
        identity = current_user.u_token

        conn = users.get_connection()

        with conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    'select * from db_jeeves.PROJECT where ref_identity = %s', (identity))
                project = cursor.fetchone()

                if project:
                    redirect('/view_project/' + identity)

        return redirect('/')

    @app.route('/view_project/<string:user_name>', methods=['GET'])
    def view_project(user_name):
        force_update = 'false'
        if request.args:
            if request.args.get('force'):
                force_update = 'true'

        identity = current_user.identity

        conn = users.get_connection()
        with conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    'select lang from db_jeeves.PROJECT where ref_identity = %s', identity)
                sql_rs = cursor.fetchone()

        lang, pth = sql_rs['lang'], os.path.join('users', identity, 'app')

        return render_template('index.html',
                               force_update=force_update,
                               script_lang=lang,
                               app_path=list_dir.map_lang_dir(lang, pth))

    @app.route('/create_project', methods=['POST'])
    def create_project():
        if request and request.json:
            lang = request.json.get('lang')

            identity = current_user.identity

            if lang == langs.PY:
                dapi.copy_py_img(identity)
            if lang == langs.JS:
                dapi.copy_js_img(identity)
            if lang == langs.PHP:
                dapi.copy_php_img(identity)

            conn = users.get_connection()
            with conn:
                with conn.cursor() as cursor:
                    try:
                        cursor.execute(
                        'insert into db_jeeves.PROJECT values(%s, %s)', (identity, lang))
                        conn.commit()
                    except:
                        cursor.execute(
                        'update db_jeeves.PROJECT set lang=%s where ref_identity=%s', (lang, identity))
                        conn.commit()


            return jsonify(['ok'])

    @app.route('/get_dir', methods=['GET', 'POST'])
    def get_dir():
        if not request.json:
            return '', 404
        if not request.json.get('dir'):
            return '', 404
        return jsonify(list_dir.list_dir(request.json['dir']))

    @ app.route('/get_file', methods=['GET', 'POST'])
    def get_file():
        f_text = None
        if request.json:
            if not request.json.get('path'):
                return '', 404
            if not os.path.exists(request.json['path']):
                return '', 404
            with open(request.json['path']) as f:
                f_text = f.read()
        if f_text:
            return jsonify({'content': f_text})
        return 'No such file', 404

    @ app.route('/get_logs/<string:user_name>', methods=['GET'])
    def get_logs(user_name):
        # return jsonify(dict({"logs" : dapi.get_container_logs(user_name)}))
        return "<p>" + dapi.get_container_logs(user_name).replace("\n", "<br>").replace(" ", "&nbsp;") + "</p>"

    @ app.route('/rm_file', methods=['GET', 'POST'])
    def rm_file():
        if request.json:
            if not request.json.get('path'):
                return '', 404
            if not os.path.exists(request.json['path']):
                return '', 404
            os.remove(request.json['path'])
        return jsonify('rm'), 200

    return app
