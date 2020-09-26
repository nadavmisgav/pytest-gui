import os
import sys
import subprocess
from dataclasses import dataclass
from multiprocessing.connection import Listener
from decouple import config

PLUGIN_PORT = config("PYTEST_GUI_PLUGIN_PORT", cast=int, default=6000)
PLUGIN_PATH = 1

def generate_messages(conn):
    while True:
        msg = conn.recv()
        if msg == 'close':
            conn.close()
            break
        yield msg
    

@dataclass()
class TestFunction():
    name: str
    marker: str = ""
    selected: bool = True

@dataclass()
class TestModule:
    name: str
    tests: list
    selected: bool = True

class PytestWorker:
    def __init__(self, test_dir):
        self.test_dir = test_dir
        self.tests = []
        self.markets = []
    
    def discover(self, filter=""):
        address = ('localhost', PLUGIN_PORT)
        listener = Listener(address)
        
        p = self._run_pytest(self.test_dir, "--collect-only")
        conn = listener.accept()
        print('connection accepted from', listener.last_accepted)
        for msg in generate_messages(conn):
            print(msg)
        listener.close()
        
        # self.tests = self._parse_discover(p.stdout) 
  
    def markers(self, filter=""):
        pass
    
    @staticmethod
    def _run_pytest(*args):
        return subprocess.Popen(['pytest', "-p", "pytest_gui.pytest.pytest_gui_plugin"] + list(args), 
                         stdout=subprocess.PIPE, 
                         universal_newlines=True)     

a = PytestWorker("/home/nadav/projects/calc_test/tests")
a.discover()
