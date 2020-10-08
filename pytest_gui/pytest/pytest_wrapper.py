import json
import logging
import os
import subprocess
from multiprocessing.connection import Listener
from queue import Queue
from threading import Thread

from decouple import config


logger = logging.getLogger('pytest_gui.backend.main')


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


class _TestRunner(Thread):
    def __init__(self, worker, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.worker = worker

    def run(self):
        try:
            while self.worker._cur_tests.poll() is None:
                output = self.worker._cur_tests.stdout.readline()
                if output != b'':
                    self.worker.log_queue.put(output.strip())
            self.worker._cur_tests.wait()

            self.worker._remove_proccess(self.worker._cur_tests.pid)
            self.worker._cur_tests = None
            self.worker.tests_running = False
            self.worker.test_stream_connection = None
        except Exception:
            if self.worker._cur_tests is not None:  # Exception raised not via kill
                raise


class _StatusUpdate(Thread):
    def __init__(self, worker, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.worker = worker

    @staticmethod
    def _generate_status(conn):
        while True:
            try:
                msg = conn.recv()
            except (EOFError, AttributeError):
                break
            yield msg

    def run(self):
        for msg in self._generate_status(self.worker.test_stream_connection):
            self.worker.status_queue.put(msg)


class PytestWorker:
    def __init__(self, test_dir):
        self.test_dir = test_dir
        self.markers = None
        self.tests_running = False
        self.test_stream_connection = None
        self._cur_tests = None
        self._listener = Listener(ADDRESS)
        self.log_queue = Queue()
        self.status_queue = Queue()
        self._process = {}

    def __del__(self):
        self._listener.close()

    def discover(self):
        p, conn = self._run_pytest(self.test_dir, "--collect-only")
        logger.debug(f'Connection accepted from {self._listener.last_accepted}')
        try:
            tests = json.loads(conn.recv())  # Only one message
        finally:
            conn.close()
            p.wait()
            self._remove_proccess(p.pid)

        if p.returncode != 0:
            logger.error(f"Failed to collect tests:\nstdout:\n{p.stdout}\nstderr\n{p.stderr}")
            return None

        logger.info(f"Collected {len(tests)} tests")
        return tests

    def get_markers(self):
        p, _ = self._run_pytest(self.test_dir, "--markers")
        p.wait()
        self._remove_proccess(p.pid)
        if p.returncode != 0:
            logger.error(f"Failed to get markers:\nstdout:\n{p.stdout}\nstderr\n{p.stderr}")
            return None

        self.markers = [{"name": name} for name, desc in _filter_only_custom_markers(p.stdout)]
        logger.info(f"Got {len(self.markers)} custom markers")
        return self.markers

    def run_tests(self, tests):
        if tests is None:
            raise RuntimeError("No tests available")

        self.tests_running = True
        pytest_arg = [test["nodeid"] for test in tests]
        p, conn = self._run_pytest(*pytest_arg)
        self._cur_tests = p
        self.test_stream_connection = conn
        _TestRunner(self).start()
        _StatusUpdate(self).start()

    def stop_tests(self):
        if self._cur_tests is None:
            raise RuntimeError("No currently running tests")

        # TODO: Race condition?
        self._cur_tests.kill()
        self.tests_running = False
        self.test_stream_connection = None
        self._remove_proccess(self._cur_tests.pid)
        self._cur_tests = None

    def _run_pytest(self, *args):
        command = ['pytest', "--capture=tee-sys", "-p", PLUGIN_PATH] + list(args)
        logger.info(f"Runing command: {' '.join(command)}")
        my_env = os.environ.copy()
        my_env["PYTHONUNBUFFERED"] = "1"
        p = subprocess.Popen(command, stdout=subprocess.PIPE, universal_newlines=True, env=my_env)
        logger.debug("Waiting for plugin connection")
        conn = self._listener.accept()
        self._process[p.pid] = p
        return p, conn

    def _remove_proccess(self, pid):
        try:
            self._process.pop(pid)
        except KeyError:
            logger.warning(f"Trying to remove non-existing pid {pid}")


worker = PytestWorker(TEST_DIR)
