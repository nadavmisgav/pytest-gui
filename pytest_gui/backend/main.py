# flake8: noqa
# autopep8: off

# This is required by the gevent server to patch code
from gevent import monkey
monkey.patch_all()

import logging
import os
import sys

import connexion

from decouple import config

from gevent.pywsgi import WSGIServer


DEBUG = config("PYTEST_GUI_DEBUG", cast=bool, default=False)
SERVER_PORT = config("PYTEST_GUI_PORT", cast=int, default=5000)
HOST = "localhost"


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'api/endpoints')))
app = connexion.FlaskApp(__name__, specification_dir='./api/')

# Set logger
logger = app.app.logger
logger.setLevel(logging.DEBUG if DEBUG else logging.INFO)
logger.handlers[0].setFormatter(logging.Formatter('[%(asctime)s]::%(levelname)s::%(message)s'))


app.add_api('swagger.yaml')
http_server = WSGIServer((HOST, SERVER_PORT), app)


@app.route('/')
def react_app():
    return "Hello world"


def cmd(argv=sys.argv):
    logger.info(f"Starting Pytest-GUI app on {HOST}:{SERVER_PORT} [DEBUG={DEBUG}]")
    try:
        http_server.serve_forever()
    except KeyboardInterrupt:
        logger.info(f"Stoping Pytest-GUI app")
        http_server.stop()


if __name__ == '__main__':
    cmd(sys.argv)
