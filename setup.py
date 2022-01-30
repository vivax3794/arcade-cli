from setuptools import setup, find_packages

setup(
    name='arcade_cli',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    py_modules=['arcade_cli'],
    install_requires=[
        'Click',
        "requests",
        "more_itertools",
        "pyjwt",
        "rich"
    ],
    entry_points={
        'console_scripts': [
            'arcade = arcade_cli.cli:arcade_cli',
        ],
    },
)