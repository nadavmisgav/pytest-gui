from pytest_gui.pytest.pytest_wrapper import worker


def select(tests):
    # connexion validates the data
    worker.tests = tests
    return worker.tests


def get():
    return worker.tests
