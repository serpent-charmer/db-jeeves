import os
from flask import Blueprint, send_from_directory, current_app

def get_blueprint():
    assets_bp = Blueprint('assets_bp', __name__,
                       template_folder='templates',
                       static_folder='static')

    @assets_bp.route('/worker-html.js', methods=['GET'])
    def get_worker_html():
        return send_from_directory(os.path.join(current_app.root_path, 'static'), 'worker-html.js')

    @assets_bp.route('/fonts/JetBrainsMono-Regular.ttf', methods=['GET'])
    def get_font():
        return send_from_directory(os.path.join(current_app.root_path, 'static'), 'JetBrainsMono-VariableFont_wght.ttf')

    @assets_bp.route('/worker-javascript.js', methods=['GET'])
    def get_worker_js():
        return send_from_directory(os.path.join(current_app.root_path, 'static'), 'worker-javascript.js')

    @assets_bp.route('/worker-php.js', methods=['GET'])
    def get_worker_php():
        return send_from_directory(os.path.join(current_app.root_path, 'static'), 'worker-php.js')

    return assets_bp