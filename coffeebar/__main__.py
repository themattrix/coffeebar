import os

from coffeebar.app import app


if __name__ == '__main__':
    app.run(
        host=os.environ.get('HOST', '127.0.0.1'),
        port=os.environ.get('PORT', 5000),
        debug=os.environ.get('DEBUG', None) == 'True')
