from dataclasses import dataclass
from pytest_gui.backend.config import DEBUG, TEST_DIR

@dataclass()
class Test():
    parent: str
    name: str
    selected: bool = True

def get():
    print(TEST_DIR)
    return [TESTS[key] for key in sorted(TESTS.keys())]