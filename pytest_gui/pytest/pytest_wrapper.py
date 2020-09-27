import os
import sys
import subprocess
import json
from dataclasses import dataclass
from multiprocessing.connection import Listener
from collections import defaultdict
from decouple import config

from pytest_gui.backend.config import DEBUG, TEST_DIR

PLUGIN_PORT = config("PYTEST_GUI_PLUGIN_PORT", cast=int, default=6000)
PLUGIN_PATH = "pytest_gui.pytest.pytest_gui_plugin"
ADDRESS = ('localhost', PLUGIN_PORT)


_builtin_markers = [
    "no_cover",
    "filterwarnings",
    "skip",
    "skipif",
    "xfail",
    "parametrize",
    "usefixtures",
    "tryfirst",
    "trylast",
]
def _filter_only_custom_markers(out):
    """Generator for parse output and return custom markers
    Args:
        out (str): output of pytest --markers
    Yields:
        tuple(str, str): contains name and description of the marker
    """
    for marker in out:
        if marker.startswith("@"):
            name = marker.split(":")[0].split(".")[2]
            desc = "".join(marker.split(":")[1:]).strip().rstrip(".")
            if any(name.startswith(marker) for marker in _builtin_markers):
                continue
            yield name, desc

        
def generate_messages(conn):
    while True:
        msg = conn.recv()
        if msg == 'close':
            conn.close()
            break
        yield msg
    

class PytestWorker:
    def __init__(self, test_dir):
        self.test_dir = test_dir
        self.modules = None
        self.markers = None
    
    def discover(self):
        # TODO: Handle errors in collect
        listener = Listener(ADDRESS)
        
        p = self._run_pytest(self.test_dir, "--collect-only")
        conn = listener.accept()
        # TODO: add logging
        print('connection accepted from', listener.last_accepted)
        
        try:
            tests = json.loads(next(generate_messages(conn))) # Only one message
        finally:
            listener.close()
        
        self.modules = self._parse_discover(tests["tests"]) 
        
    @staticmethod
    def _parse_discover(tests):
        modules = defaultdict(list)
        for test in tests:
            id_ = test["id"]
            line = test["line"]
            module, name = id_.split("::")
            modules[module].append({"name": name, "line": line, "selected": True})
        return modules
        
    def get_markers(self):
        # TODO: Handle errors in markers
        p = self._run_pytest(self.test_dir, "--markers")
        self.markers = [{"name": name, "description": desc} for name, desc in _filter_only_custom_markers(p.stdout)]
            
    @staticmethod
    def _run_pytest(*args):
        return subprocess.Popen(['pytest', "-p", PLUGIN_PATH] + list(args), 
                         stdout=subprocess.PIPE, 
                         universal_newlines=True)     


worker = PytestWorker(TEST_DIR)

if __name__ == "__main__":
    a = PytestWorker("/home/nadav/projects/calc_test/tests")
    a.get_markers()
    print(a.markers)
