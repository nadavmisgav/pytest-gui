import py
import sys
import pytest
import json
import subprocess
from multiprocessing.connection import Client
from decouple import config
from contextlib import contextmanager
from datetime import datetime
import os
from os.path import join


PLUGIN_PORT = config("PYTEST_GUI_PLUGIN_PORT", cast=int, default=6000)
REPORT_DIR= config("PYTEST_GUI_REPORT_DIR", default=".reports")

ADDRESS = ('localhost', PLUGIN_PORT)


collected_errors = []

def get_line_number(item):
    location = getattr(item, 'location', None)
    if location is not None:
        return location[1]
    obj = getattr(item, 'obj', None)
    if obj is not None:
        try:
            from _pytest.compat import getfslineno
            return getfslineno(obj)[1]
        except:
            pass
    return None

def extract_discovered_tests(session):
    tests = []
    for item in session.items:
        line = get_line_number(item)
        tests.append({'id': item.nodeid,
                        'line': line})
    return tests

def extract_discovery_errors():
    errors = []
    for error in collected_errors:
        try:
            errors.append({'file': error.location[0] if error.location else None,
                            'message': error.longreprtext})
        except:
            pass
    return errors


class PytestGuiPlugin:    
    def __init__(self):
        self._conn = Client(ADDRESS)
        self._report_folder = ""
    
    def __del__(self):
        self._conn.send('close')
        self._conn.close()
        
    def pytest_collection_finish(self, session):
        tests = extract_discovered_tests(session)
        errors = extract_discovery_errors()
        self._conn.send(json.dumps({'tests': tests, 'errors': errors}))

    def pytest_collectreport(self, report):
        if report.failed:
            collected_errors.append(report)

    def pytest_runtestloop(self, session):
        timestamp = datetime.now().strftime("%d_%m_%Y__%H_%M_%S")
        self._report_folder = join(REPORT_DIR, timestamp)
        os.makedirs(self._report_folder, exist_ok=False)
        
    def pytest_runtest_logreport(self, report):
        # Send result
        self._conn.send(json.dumps({
            'when': report.when,
            'outcome': report.outcome,
            "nodeid": report.nodeid,
            "duration": report.duration
            }))
    
        # Log output
        folder, test = report.nodeid.split("/")
        module, id_ = test.split("::")
        
        log_folder = join(self._report_folder, folder, module) 
        os.makedirs(log_folder, exist_ok=True)
        
        log_file = join(log_folder, f"{id_}.log")
        with open(log_file, "a") as fp:
            fp.write(f"{report.when}\n")
            for section in report.sections:
                fp.writelines(section)


def pytest_configure(config):
    config.pluginmanager.register(PytestGuiPlugin())