# Setuptools
# http://flask.pocoo.org/docs/0.12/patterns/packages/
# http://flask.pocoo.org/docs/0.12/patterns/distribute/


from setuptools import setup


setup(
    name='taberu_admin',
    packages=['taberu_admin'],
    install_requires=[
        'flask>=0.12.2',
        'flask-login>=0.4.1',
        'flask-sqlalchemy>=2.3.2',
        'flask-wtf>=0.14.2',
        'jinja2>=2.10',
        'MarkupSafe>=1.0',
        'SQLAlchemy>=1.1.15',
        'WTForms>=2.1',
        'Werkzeug>=0.13',
        'click>=6.7',
        'itsdangerous>=0.24',
        'pip>=9.0.1',
        'psycopg2>=2.7.3.2',
        'setuptools>=38.2.4',
        'wheel>=0.30.0',
        'pytz>=2018.3'
    ]
)