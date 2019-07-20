"""Setup script for the TROLS Stats project.
"""
import setuptools


PACKAGES = [
    'configa>=1.0.0',
    'dropbox>=7.2.1',
    'filer>=1.0.0',
    'lxml>=3.7.2',
    'pylint>=1.6.4',
    'pytest>=2.9.2',
    'pytest-cov>=2.3.0',
    'sphinx_rtd_theme>=0.1.10a0',
    'twine',
    'Sphinx>=1.4.5',
]

SETUP_KWARGS = {
    'name': 'trols-stats',
    'version': '1.0.2',
    'description': 'TROLS statistics data model and utils',
    'author': 'Lou Markovski',
    'author_email': 'lou.markovski@gmail.com',
    'url': 'https://github.com/loum/trols-stats',
    'install_requires': PACKAGES,
    'packages': setuptools.find_packages(),
    'package_data': {
        'trols_stats': [
        ],
    },
    'license': 'MIT',
    'classifiers': [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
}

setuptools.setup(**SETUP_KWARGS)
