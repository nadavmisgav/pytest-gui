from queue import Empty

from flask import Response

from pytest_gui.pytest.pytest_wrapper import worker


def generate_from_queue(worker, queue):
    while worker.tests_running:
        # timeout is a must otherwise we never leave loop
        try:
            yield queue.get(timeout=1)
        except Empty:
            pass


def status():
    if worker.tests_running:
        return Response(generate_from_queue(worker, worker.status_queue), mimetype="text/event-stream")
    else:
        return Response(status=400, response="Not tests are currently running")


def logs():
    if worker.tests_running:
        return Response(generate_from_queue(worker, worker.log_queue), mimetype="text/event-stream")
    else:
        return Response(status=400, response="Not tests are currently running")
