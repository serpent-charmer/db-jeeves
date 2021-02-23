import os
from flask import Flask, session, render_template, jsonify, request, flash, redirect, session, current_app, send_from_directory
from . import dapi, list_dir


def get_app():
	app = Flask(__name__, static_url_path='/static')
	app.secret_key = 'xxx_secret_xxx'
#	login_manager = LoginManager()
#	login_manager.init_app(app)

	@app.route('/', methods=['GET'])
	def main():
		return '', 501

	@app.route('/create_project/<string:user_name>', methods=['GET'])
	def create_project(user_name):
		# TODO user_name
		nm = 'new-user-312315fwefg3459'
		slang, pth = dapi.copy_py_img(nm)
		#container = dapi.build_custom_img(nm_path, nm)
		#port = container.ports['8000/tcp'][0]['HostPort']
		print(pth)
		return render_template('index.html', script_lang=slang, app_path=os.path.join(pth, 'app'))
		# return '<h1>Container started at port: {0}</h1><h2><a href="http://192.168.31.217:{0}">Goto</a></h2>'.format(port)

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
				return "", 404
			if not os.path.exists(request.json['path']):
				return "", 404
			with open(request.json['path']) as f:
				f_text = f.read()
		if f_text:
			return jsonify({'content': f_text})  # request.json
		return 'No such file'
	return app
