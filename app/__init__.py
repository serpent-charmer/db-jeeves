import os
from flask import Flask, session, render_template, jsonify, request, flash, redirect, session, current_app, send_from_directory
from distutils.dir_util import remove_tree
from . import dapi, list_dir

import pymysql.cursors
from pymysql.constants import CLIENT

def get_connection(db_user, db_name):
    connection = pymysql.connect(host='localhost',
                             user=db_user,
                             password=os.environ['MYSQL_ROOT_PWD'],
                             db=db_name,
                             charset='utf8mb4',
                             client_flag=CLIENT.MULTI_STATEMENTS,
                             cursorclass=pymysql.cursors.DictCursor)
    return connection

def get_root_connection():
    connection = pymysql.connect(host='localhost',
                             user='root_doormat',
                             password='',
                             charset='utf8mb4',
                             client_flag=CLIENT.MULTI_STATEMENTS,
                             cursorclass=pymysql.cursors.DictCursor)
    return connection

def get_app():
	app = Flask(__name__, static_url_path='/static')
	app.secret_key = 'xxx_secret_xxx'
#	login_manager = LoginManager()
#	login_manager.init_app(app)

	@app.route('/', methods=['GET'])
	def main():
		return render_template('main.html')

	@app.route('/test', methods=['POST'])
	def test():
		return jsonify(dict({"pwd" : os.environ['MYSQL_ROOT_PWD']}))

	@app.route('/sync_changes', methods=['POST'])
	def sync_changes():
		if not request and not request.json:
			return '',404
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
			return jsonify({'port' : port})
		return '',404



	@app.route('/create_project', methods=['POST'])
	def create_project():
		if request and request.json:
			lang = request.json.get('lang')
			usr = request.json.get('usr')

			conn = get_root_connection()

			#with conn.cursor() as cursor:
			#	cursor.execute("CREATE DATABASE IF NOT EXISTS " + usr)
				
			conn.close()

			if lang == 'py':
				dapi.copy_py_img(usr)
			if lang == 'js':
				dapi.copy_js_img(usr)
			if lang == 'php':
				dapi.copy_php_img(usr)

			return jsonify(['ok'])
			#render_template('index.html', force_update='true', script_lang=slang, usr=nm, app_path=os.path.join(pth, 'app'))
		# return '<h1>Container started at port: {0}</h1><h2><a href="http://192.168.31.217:{0}">Goto</a></h2>'.format(port)

	@app.route('/view_project/<string:user_name>', methods=['GET'])
	def view_project(user_name):
		force_update = 'false'
		if request.args:
			if request.args.get('force'):
				force_update = 'true'
		nm = user_name
		slang, pth = 'python', os.path.join('users', nm)
		#container = dapi.build_custom_img(nm_path, nm)
		#port = container.ports['8000/tcp'][0]['HostPort']
		return render_template('index.html', force_update=force_update, script_lang=slang, usr=nm, app_path=os.path.join(pth, 'app'))

	@app.route('/test_user', methods=['GET'])
	def test_user():
		return redirect('/view_project/new-user-312315fwefg3459')

	@app.route('/get_dir', methods=['GET', 'POST'])
	def get_dir():
		if not request.json:
			return '', 404
		if not request.json['dir']:
			return '', 404
		return jsonify(list_dir.list_dir(request.json['dir']))

	@app.route('/get_file', methods=['GET', 'POST'])
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

	@app.route('/get_logs/<string:user_name>', methods=['GET'])
	def get_logs(user_name):
		#return jsonify(dict({"logs" : dapi.get_container_logs(user_name)}))
		return "<p>" + dapi.get_container_logs(user_name).replace("\n", "<br>").replace(" ", "&nbsp;") + "</p>"

	@app.route('/rm_file', methods=['GET', 'POST'])
	def rm_file():
		f_text = None
		if request.json:
			if not request.json.get('path'):
				return '', 404
			if not os.path.exists(request.json['path']):
				return '', 404
			os.remove(request.json['path'])
		return jsonify('rm'), 200





	return app


