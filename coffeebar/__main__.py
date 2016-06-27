import os

from coffeebar.app import app


if __name__ == '__main__':
    app.run(host=os.environ.get('FLASK_HOST', '127.0.0.1'), debug=os.environ.get('FLASK_DEBUG', None) == 'True')
