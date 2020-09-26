import sys
import os
import connexion

from .config import DEBUG, SERVER_PORT


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'api/endpoints')))
app = connexion.App(__name__, specification_dir='./api/')
app.add_api('swagger.yaml')

@app.route('/')
def react_app():
    return "Hello world"

def cmd(argv=sys.argv):
    # if len(argv) != 2:
    #     print("usage pytest-gui test_dir")
    app.run(host='0.0.0.0', port=SERVER_PORT, debug=DEBUG)
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=SERVER_PORT, debug=DEBUG)