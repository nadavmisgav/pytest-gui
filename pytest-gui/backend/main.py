import sys
import os
import connexion
from decouple import config

PYTEST_GUI_DEBUG = config("PYTEST_GUI_DEBUG", cast=bool, default=False)
PYTEST_GUI_PORT = config("PYTEST_GUI_PORT", cast=int, default=5000)


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'api/endpoints')))


app = connexion.App(__name__, specification_dir='./api/')
app.add_api('swagger.yaml')

@app.route('/')
def home():
    return "Hello world"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PYTEST_GUI_PORT, debug=PYTEST_GUI_DEBUG)