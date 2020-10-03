from queue import Empty

from flask import Response

from gevent import sleep

from pytest_gui.pytest.pytest_wrapper import worker


def generate_status(conn):
    while True:
        try:
            msg = conn.recv()
        except BlockingIOError:  # recv is not blocking
            sleep(1)  # balance number of receives
            continue
        except EOFError:
            break

        yield msg


def generate_logs(worker):
    while worker.tests_running:
        # timeout is a must otherwise we never leave loop
        try:
            yield worker.log_queue.get(timeout=1)
        except Empty:
            pass


def status():
    if worker.tests_running:
        return Response(generate_status(worker.test_stream_connection), mimetype="text/event-stream")
    else:
        return Response(status=503, response="Not tests are currently running")


def logs():
    if worker.tests_running:
        return Response(generate_logs(worker), mimetype="text/event-stream")
    else:
        return Response(status=503, response="Not tests are currently running")
