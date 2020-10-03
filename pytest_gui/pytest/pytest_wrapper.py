import os
import sys
import json
import logging
import subprocess

from dataclasses import dataclass
from multiprocessing.connection import Listener
from threading import Thread
from collections import defaultdict
from decouple import config
from queue import Queue


logger = logging.getLogger('main')


TEST_DIR = config("PYTEST_GUI_TEST_DIR", default=".")
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

        
class TestRunner(Thread):
    def run(self, worker):
        try:
            while worker._cur_tests.poll() is None:
                output = worker._cur_tests.stdout.readline()
                if output != b'':
                    worker.log_queue.put(output.strip())
            worker._cur_tests.wait()
            
            worker._cur_tests = None
            worker.tests_running = False
            worker.test_stream_connection = None
        except:
            if worker._cur_tests != None: # Exception raised not via kill
                raise


class PytestWorker:
    def __init__(self, test_dir):
        self.test_dir = test_dir
        self.modules = None
        self.markers = None
        self.tests_running = False
        self.test_stream_connection = None
        self._cur_tests = None
        self._listener = Listener(ADDRESS)
        self.log_queue = Queue()
    
    def __del__(self):
        self._listener.close()
    
    def discover(self):
        p, conn = self._run_pytest(self.test_dir, "--collect-only")
        logger.debug(f'Connection accepted from {self._listener.last_accepted}')
        try:
            tests = json.loads(conn.recv()) # Only one message
        finally:
            conn.close()
            p.wait()

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
        p, _ = self._run_pytest(self.test_dir, "--markers")
        self.markers = [{"name": name, "description": desc} for name, desc in _filter_only_custom_markers(p.stdout)]
            
    def run_tests(self):
        pytest_arg = []
        for module, tests in self.modules.items():
            for test in tests:
                if test["selected"]:
                    pytest_arg.append(f"{module}::{test['name']}")
        
        p, conn = self._run_pytest(*pytest_arg)
        self._cur_tests = p
        self.tests_running = True
        self.test_stream_connection = conn
        TestRunner().run(self)
        
    def stop_tests(self):
        self._cur_tests.kill()
        self._cur_tests = None
        self.tests_running = False
        self.test_stream_connection = None

    def _run_pytest(self, *args):
        command = ['pytest', "--capture=tee-sys", "-p", PLUGIN_PATH] + list(args)
        logger.info(f"Runing command: {' '.join(command)}")        
        p = subprocess.Popen(command, stdout=subprocess.PIPE, universal_newlines=True)
        logger.debug("Waiting for plugin connection")
        conn = self._listener.accept()
        return p, conn

worker = PytestWorker(TEST_DIR)
