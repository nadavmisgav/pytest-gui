import os
import sys
import subprocess
import json
from dataclasses import dataclass
from multiprocessing.connection import Listener
from collections import defaultdict
from decouple import config

PLUGIN_PORT = config("PYTEST_GUI_PLUGIN_PORT", cast=int, default=6000)
PLUGIN_PATH = "pytest_gui.pytest.pytest_gui_plugin"

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
        self.tests = None
        self.markers = None
    
    def discover(self, filter=""):
        address = ('localhost', PLUGIN_PORT)
        listener = Listener(address)
        
        p = self._run_pytest(self.test_dir, "--collect-only")
        conn = listener.accept()
        # TODO: add logging
        print('connection accepted from', listener.last_accepted)
        tests = json.loads(next(generate_messages(conn))) # Only one message
        listener.close()
        
        self.tests = self._parse_discover(tests["tests"]) 
        # TODO: Handle errors in collect
        
    @staticmethod
    def _parse_discover(tests):
        modules = defaultdict(list)
        for test in tests:
            id_ = test["id"]
            line = test["line"]
            module, name = id_.split("::")
            modules[module].append({"name": name, "line": line, "selected": True})
        return modules
        
  
    def markers(self, filter=""):
        pass
    
    @staticmethod
    def _run_pytest(*args):
        return subprocess.Popen(['pytest', "-p", PLUGIN_PATH] + list(args), 
                         stdout=subprocess.PIPE, 
                         universal_newlines=True)     

a = PytestWorker("/home/nadav/projects/calc_test/tests")
a.discover()
