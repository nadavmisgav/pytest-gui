from __future__ import print_function

import json
import os
from datetime import datetime
from multiprocessing.connection import Client
from os.path import join

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
REPORT_DIR = config("PYTEST_GUI_REPORT_DIR", default=".reports")

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
        self._report_folder = ""

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

    def pytest_runtestloop(self, session):
        timestamp = datetime.now().strftime("%d_%m_%Y__%H_%M_%S")
        self._report_folder = join(REPORT_DIR, timestamp)
        try:
            os.makedirs(self._report_folder)
        except OSError:
            pass

    def pytest_runtest_logreport(self, report):
        # Send result
        self._conn.send(json.dumps({
            'when': report.when,
            'outcome': report.outcome,
            "nodeid": report.nodeid,
            "duration": str(report.duration)
        }))

        # Log output
        folder, test = report.nodeid.split("/")
        module, id_ = test.split("::")

        log_folder = join(self._report_folder, folder, module)
        os.makedirs(log_folder, exist_ok=True)

        log_file = join(log_folder, "{}.log".format(id_))
        with open(log_file, "a") as fp:
            fp.write(report.when + "\n")
            for section in report.sections:
                fp.writelines(section)


def pytest_configure(config):
    config.pluginmanager.register(PytestGuiPlugin())
