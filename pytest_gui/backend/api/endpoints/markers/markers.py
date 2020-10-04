
from flask import Response

from pytest_gui.pytest.pytest_wrapper import worker


def get():
    markers = worker.get_markers()
    if markers is None:
        return Response(status=500, response="Failed to get markers, check log")
    else:
        return markers
