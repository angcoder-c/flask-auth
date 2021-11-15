import os

app_dir = os.path.abspath(os.path.dirname(__file__))

class DefaultConfig:
    SECRET_KEY = 'SUPER_SECRET'
    DEBUG = True
    TESTING = False
    SQLALCHEMY_DATABASE_URI= 'sqlite:///' + os.path.join(app_dir, 'app/schema.db').replace('\\', '/')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevConfig(DefaultConfig):
    DEBUG = True
    TESTING = True

class TestConfig(DefaultConfig):
	TESTING = True

class ProdConfig(DefaultConfig):
    DEBUG = False
    TESTING = False