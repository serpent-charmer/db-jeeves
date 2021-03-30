import os

from flask import Flask, make_response, render_template, url_for, jsonify, request, redirect, session, current_app, send_from_directory
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from distutils.dir_util import remove_tree
from . import dapi, list_dir, langs, users, mvars


def get_app():
    app = Flask(__name__, static_url_path='/static')
    app.secret_key = 'xxx_secret_xxx'

    with app.app_context():
        from . import schemes
        from . import auth
        app.register_blueprint(schemes.get_blueprint())
        app.register_blueprint(auth.get_blueprint())

    @app.route('/favicon.ico', methods=['GET'])
    def favicon():
        return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico')

    @app.route('/', methods=['GET'])
    @login_required
    def main():
        return render_template('main.html')

    @app.route('/worker-html.js', methods=['GET'])
    def get_worker_html():
        return send_from_directory(os.path.join(app.root_path, 'static'), 'worker-html.js')

    @app.route('/worker-javascript.js', methods=['GET'])
    def get_worker_js():
        return send_from_directory(os.path.join(app.root_path, 'static'), 'worker-javascript.js')

    @app.route('/worker-php.js', methods=['GET'])
    def get_worker_php():
        return send_from_directory(os.path.join(app.root_path, 'static'), 'worker-php.js')

    @app.route('/sync_changes', methods=['POST'])
    def sync_changes():
        if not request and not request.json:
            return '', 404
        for entr in request.json.items():
            dpath, changed = entr
            with open(dpath, 'w+') as f:
                f.write(changed)
        return jsonify(['ok'])

    @app.route('/restart_instance', methods=['POST'])
    def restart_instance():
        if request and request.json.get('user'):

            nm = request.json['user']
            container = dapi.build_custom_img(os.path.join('users', nm), nm)
            port = dapi.get_container_port(container)

            conn = users.get_connection()

            with conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        'UPDATE db_jeeves.PROJECT SET last_port=%s where ref_identity=%s', (port, nm))
                    conn.commit()

            return jsonify({'port': port})
        return '', 404

    @app.route('/view_project/<string:identity>', methods=['GET'])
    def view_project_ref(identity):

        last_port = None

        conn = users.get_connection()

        with conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    'SELECT last_port FROM db_jeeves.PROJECT where ref_identity=%s', (identity))
                last_port_tuple = cursor.fetchone()
                last_port = (last_port_tuple and last_port_tuple.get(
                    'last_port')) or None

        if last_port:
            host_ip = request.host.split(":")[0]
            return redirect('http://' + host_ip + ':' + str(last_port))
        else:
            return '<h1>Not Found<h1><h2>No project hosted for this user</h2>'

    @app.route('/view_project', methods=['GET'])
    def view_project():
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

        lang, pth = sql_rs and sql_rs['lang'], os.path.join(
            'users', identity, 'app')

        if not lang:
            return '<h1>Not Found<h1><h2>No project created for this user</h2>'

        has_diagram = os.path.exists(os.path.join(
            os.getcwd(), 'users', identity, identity+".pdf"))

        return render_template('index.html',
                               has_diagram=has_diagram,
                               force_update=force_update,
                               script_lang=lang,
                               app_path=list_dir.map_lang_dir(lang, pth))

    @app.route('/create_project', methods=['POST'])
    def create_project():
        if request and request.json:
            lang = request.json.get('lang')
            vendor = request.json.get('vendor')

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
                            'insert into db_jeeves.PROJECT values(%s, %s, %s, %s)', (identity, lang, vendor, None))
                        conn.commit()
                    except:
                        cursor.execute(
                            'update db_jeeves.PROJECT set lang=%s, db_vendor=%s where ref_identity=%s', (lang, vendor, identity))
                        conn.commit()

            return jsonify('ok')

    @app.route('/get_diagram_mysql', methods=['GET'])
    def get_diagram():
        os.system('''
        schemacrawler --server=mysql --database="{0}db" -schemas=."{0}db"..dbo \
        --host={1} --user={0} --password=abc --info-level=maximum \
        -c=schema --output-format=pdf -o=users/{0}/{0}.pdf "$*"
        '''.format(current_user.identity, mvars.MY_SQL_IP))
        return redirect(url_for('.view_diagram'))

    @app.route('/get_diagram_pg', methods=['GET'])
    def get_diagram_pg():
        os.system('''
        schemacrawler --server=postgresql --database="{0}db" -schemas=."{0}db"..dbo \
        --host={1} --user={0} --password=abc --info-level=maximum \
        -c=schema --output-format=pdf -o=users/{0}/{0}.pdf "$*"
        '''.format(current_user.identity, mvars.PG_SQL_IP))
        return redirect(url_for('.view_diagram'))

    @app.route('/view_diagram', methods=['GET'])
    def view_diagram():

        identity = current_user.identity
        pth = os.path.join(os.getcwd(), 'users', identity)

        response = make_response(send_from_directory(pth, identity+".pdf"))

        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'

        
        return response

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

    @ app.route('/get_logs', methods=['GET'])
    def get_logs():
        identity = current_user.identity
        log = None
        try:
            log = dapi.get_container_logs(identity)
        except:
            pass
        log = (log and log.replace("\n", "<br>").replace(
            " ", "&nbsp;")) or "Container offline"
        return render_template('logs.html', log=log)

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
