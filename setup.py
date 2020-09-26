from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    install_requires=[
        "attrs==20.2.0",
        "certifi==2020.6.20",
        "chardet==3.0.4",
        "click==7.1.2",
        "clickclick==1.2.2",
        "connexion[swagger-ui]==2.7.0",
        "flask==1.1.2",
        "idna==2.10",
        "inflection==0.5.1",
        "itsdangerous==1.1.0",
        "jinja2==2.11.2",
        "jsonschema==3.2.0",
        "markupsafe==1.1.1",
        "openapi-spec-validator==0.2.9",
        "pyrsistent==0.17.3",
        "python-decouple==3.3",
        "pyyaml==5.3.1",
        "requests==2.24.0",
        "six==1.15.0",
        "swagger-ui-bundle==0.0.8",
        "urllib3==1.25.10",
        "werkzeug==1.0.1",
    ],
    name="pytest_gui",
    version="0.0.1",
    author="ned3144",
    author_email="nadav.misgav@gmail.com",
    description="A GUI for pytest",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ned3144/pytest-gui",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    entry_points={"console_scripts": ["pytest-gui=pytest_gui.backend.main:cmd"]},
)
