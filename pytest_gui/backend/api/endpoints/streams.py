from flask import Response

# from pytest_gui.backend.main import app
from pytest_gui.pytest.pytest_wrapper import worker

def generate_status(conn):
    while True:
        try:
            msg = conn.recv()
        except EOFError:
            break
            
        if msg == 'close':
            conn.close()
            break
        yield msg
        
def generate_logs(queue):
    while True:
        yield queue.get()
        
def status():
    if worker.tests_running:
        return Response(generate_status(worker.test_stream_connection), mimetype="text/event-stream")
    else:
        return Response(status=503, response="Not tests are currently running")
    
def logs():
    if worker.tests_running:
        return Response(generate_logs(worker.log_queue), mimetype="text/event-stream")
    else:
        return Response(status=503, response="Not tests are currently running")
