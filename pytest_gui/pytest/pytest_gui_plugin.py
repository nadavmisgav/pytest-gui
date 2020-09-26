import py
import sys
import pytest
import json
import subprocess
from multiprocessing.connection import Client
from decouple import config
from contextlib import contextmanager


PLUGIN_PORT = config("PYTEST_GUI_PLUGIN_PORT", cast=int, default=6000)

@contextmanager
def client(address):
    conn = Client(address)
    yield conn
    
    conn.send('close')
    conn.close()
    
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

def pytest_collection_finish(session):
    address = ('localhost', PLUGIN_PORT)
    with client(address) as conn:
        tests = extract_discovered_tests(session)
        errors = extract_discovery_errors()
        conn.send(json.dumps({'tests': tests, 'errors': errors}))

def pytest_collectreport(report):
    if report.failed:
        collected_errors.append(report)
