from pytest_gui.pytest.pytest_wrapper import worker


def get():
    worker.discover()
    return worker.modules
