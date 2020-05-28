import os
# ENVIRONMENT = 'dev'
ENVIRONMENT = 'prod'
basedir = os.path.abspath(os.path.dirname(__file__))
class Config(object):
    if ENVIRONMENT == 'prod':
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    else:
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir,'db.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = False