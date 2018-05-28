"""
    Setuptools
    http://flask.pocoo.org/docs/0.12/patterns/packages/
    http://flask.pocoo.org/docs/0.12/patterns/distribute/
"""

from setuptools import setup


setup(
    name='taberu_admin',
    packages=['taberu_admin'],
    install_requires=[
        'flask>=1.0.2',
        'flask-login>=0.4.1',
        'flask-wtf>=0.14.2',
        'jinja2>=2.10',
        'MarkupSafe>=1.0',
        'SQLAlchemy>=1.2.7',
        'WTForms>=2.1',
        'Werkzeug>=0.14.1',
        'click>=6.7',
        'itsdangerous>=0.24',
        'psycopg2>=2.7.4',
        'pytz>=2018.4',
        'setuptools>=39.1.0',
        'six>=1.11.0',
        'wheel>=0.31.0'
    ]
)