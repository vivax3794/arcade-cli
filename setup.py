# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['arcade_cli']

package_data = \
{'': ['*']}

install_requires = \
['PyJWT>=2.3.0,<3.0.0',
 'click>=8.0.3,<9.0.0',
 'more-itertools>=8.12.0,<9.0.0',
 'poetry2setup>=1.0.0,<2.0.0',
 'requests>=2.27.1,<3.0.0',
 'rich>=11.1.0,<12.0.0']

entry_points = \
{'console_scripts': ['arcade = arcade_cli.cli:arcade_cli']}

setup_kwargs = {
    'name': 'arcade-cli',
    'version': '0.2.0',
    'description': 'A tool for interacting with the matise arcade',
    'long_description': None,
    'author': 'vivax',
    'author_email': 'vivax3794@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

