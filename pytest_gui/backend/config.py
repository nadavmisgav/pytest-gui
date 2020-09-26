from decouple import config


DEBUG = config("PYTEST_GUI_DEBUG", cast=bool, default=False)
SERVER_PORT = config("PYTEST_GUI_PORT", cast=int, default=5000)
TEST_DIR = config("PYTEST_GUI_TEST_DIR", default=".")