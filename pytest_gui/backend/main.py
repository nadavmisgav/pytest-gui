import sys
import os
import connexion

from .config import DEBUG, SERVER_PORT


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'api/endpoints')))
app = connexion.App(__name__, specification_dir='./api/')
app.add_api('swagger.yaml')

@app.route('/')
def home():
    return "Hello world"

def cmd(argv=sys.argv):
    print(f"Args: {sys.argv}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=SERVER_PORT, debug=DEBUG)