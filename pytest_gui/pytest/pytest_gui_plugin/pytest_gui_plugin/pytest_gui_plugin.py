from __future__ import print_function

import json
from multiprocessing.connection import Client


try:
    from decouple import config
except ImportError:
    from os import environ

    def config(name, cast=None, default=None):
        if name in environ:
            return cast(environ[name]) if cast else environ[name]
        if default:
            return default
        raise ValueError("Can't find {}".format(name))


PLUGIN_PORT = config("PYTEST_GUI_PLUGIN_PORT", cast=int, default=6000)

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


class PytestGuiPlugin(object):
    def __init__(self):
        self._conn = Client(ADDRESS)

    def __del__(self):
        self._conn.send('close')
        self._conn.close()

    def pytest_runtest_logstart(self, nodeid, location):
        self._conn.send(json.dumps({
            'when': "started",
            'outcome': "",
            "nodeid": nodeid,
            "duration": ""
        }))

    def pytest_collection_finish(self, session):
        self._conn.send(json.dumps([{
            "nodeid": item.nodeid,
            "id": item.name,
            "module": item.location[0].split("/")[0] if "/" in item.location[0] else "",
            "file": item.location[0].split("/")[1] if "/" in item.location[0] else item.location[0],
            "markers": [marker.name for marker in item.own_markers if marker.name not in _builtin_markers],
        } for item in session.items]))

    def pytest_runtest_logreport(self, report):
        # Send result
        self._conn.send(json.dumps({
            'when': report.when,
            'outcome': report.outcome,
            "nodeid": report.nodeid,
            "duration": str(report.duration)
        }))


def pytest_configure(config):
    config.pluginmanager.register(PytestGuiPlugin())
