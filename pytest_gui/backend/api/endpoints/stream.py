from flask import Response

# from pytest_gui.backend.main import app
from pytest_gui.pytest.pytest_wrapper import worker, generate_messages


# @app.route('/stream')
def stream():
    if worker.tests_running:
        return Response(generate_messages(worker.test_stream_connection), mimetype="text/event-stream")
    else:
        return Response(status=503, response="Not tests are currently running")
