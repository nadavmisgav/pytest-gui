from flask import Response

from pytest_gui.pytest.pytest_wrapper import worker


def get():
    tests = worker.discover()
    if tests is None:
        return Response(status=500, response="Failed to collect tests, check log")
    else:
        return tests
