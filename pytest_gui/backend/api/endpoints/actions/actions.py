from flask import Response

from pytest_gui.pytest.pytest_wrapper import worker


def discover():
    tests = worker.discover()
    if tests is None:
        return Response(status=500, response="Failed to collect tests, check log")
    else:
        return tests


def run_tests(tests):
    try:
        worker.run_tests(tests)
    except RuntimeError as e:
        return Response(status=500, response=str(e))
    return Response(status=200, response="Started running tests")


def stop_tests():
    try:
        worker.stop_tests()
    except RuntimeError as e:
        return Response(status=500, response=str(e))
    return Response(status=200, response="Stopped currently running tests")
