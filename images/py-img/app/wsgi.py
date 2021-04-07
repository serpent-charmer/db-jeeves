from app import create_app

_app = create_app()

if __name__ == '__main__':
    _app.run(host='0.0.0.0', port=8000, debug=False)
