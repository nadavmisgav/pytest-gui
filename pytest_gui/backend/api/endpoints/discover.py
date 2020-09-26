
from pytest_gui.backend.config import DEBUG, TEST_DIR
from pytest_gui.pytest.pytest_wrapper import PytestWorker

worker = PytestWorker(TEST_DIR)
def get():
    worker.discover()
    return worker.tests
    
    