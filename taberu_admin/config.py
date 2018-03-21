# Configuration Handling
# http://flask.pocoo.org/docs/0.12/config/


class Config(object):
    DEBUG = False
    TESTING = False
    DATABASE_URI = ''


class ProductionConfig(Config):
    DATABASE_URI = ''


class DevelopmentConfig(Config):
    DEBUG = True
    DATABASE_URI = 'postgresql://postgres:12344@localhost:5435/nell02_test'


class TestingConfig(Config):
    TESTING = True
