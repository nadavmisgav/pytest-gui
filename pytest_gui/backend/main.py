import logging
import os
import sys
from pathlib import Path


import connexion

from decouple import config

from prance import ResolvingParser

from waitress import serve


DEBUG = config("PYTEST_GUI_DEBUG", cast=bool, default=False)
SERVER_PORT = config("PYTEST_GUI_PORT", cast=int, default=5000)
HOST = "localhost"


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'api/endpoints')))
app = connexion.FlaskApp(__name__, specification_dir='./api/')

# Set logger
logger = app.app.logger
logger.setLevel(logging.DEBUG if DEBUG else logging.INFO)
logger.handlers[0].setFormatter(logging.Formatter('[%(asctime)s]::%(levelname)s::%(message)s'))
logger.propagate = False


def get_bundled_specs(main_file):
    parser = ResolvingParser(str(main_file.absolute()),
                             lazy=True, backend='openapi-spec-validator')
    parser.parse()
    return parser.specification


app.add_api(get_bundled_specs(Path("openapi.yaml")))


@app.route('/')
def react_app():
    return "Hello world"


def cmd(argv=sys.argv):
    logger.info(f"Starting Pytest-GUI app on {HOST}:{SERVER_PORT} [DEBUG={DEBUG}]")
    serve(app, host=HOST, port=SERVER_PORT)


if __name__ == '__main__':
    cmd(sys.argv)
