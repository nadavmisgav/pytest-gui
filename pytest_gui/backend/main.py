import logging
import os
import sys


import connexion

from decouple import config

from waitress import serve


LOG_LEVEL = config("PYTEST_GUI_LOG_LEVEL", default="INFO")
SERVER_PORT = config("PYTEST_GUI_PORT", cast=int, default=5000)
HOST = "localhost"


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'api/endpoints')))
app = connexion.FlaskApp(__name__, specification_dir='./api/')

# Set logger
logger = app.app.logger
logger.setLevel(LOG_LEVEL)
logger.handlers[0].setFormatter(logging.Formatter('[%(asctime)s]::%(levelname)s::%(message)s'))
logger.propagate = False


app.add_api("openapi.all.yaml")


@ app.route('/')
def react_app():
    return "Hello world"


def cmd(argv=sys.argv):
    logger.info(f"Starting Pytest-GUI app on {HOST}:{SERVER_PORT} [LOG_LEVEL={logging.getLevelName(logger.level)}]")
    serve(app, host=HOST, port=SERVER_PORT)


if __name__ == '__main__':
    cmd(sys.argv)
