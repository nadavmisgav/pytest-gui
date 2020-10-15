from setuptools import find_packages, setup

setup(
    install_requires=[],
    name="pytest_gui_plugin",
    version="0.0.1",
    author="ned3144",
    description="A plugin for pytest-gui",
    url="https://github.com/ned3144/pytest-gui",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language:: Python:: 2",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=2.7",
)
