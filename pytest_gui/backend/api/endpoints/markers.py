
from pytest_gui.pytest.pytest_wrapper import worker


def get():
    worker.get_markers()
    return worker.markers
