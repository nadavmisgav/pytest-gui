from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    install_requires=[],
    name="pytest-gui",
    version="0.0.1",
    author="ned3144",
    author_email="nadav.misgav@gmail.com",
    description="A GUI for pytest",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ned3144/pytest-gui",
    packages="pytest-gui",
    package_data={"pytest-gui": ["resources/*", "public/*"]}
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
