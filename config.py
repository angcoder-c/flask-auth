import os

root_dir = os.path.abspath(os.path.dirname(__file__)).replace('\\', '/')

class DefaultConfig:
    SECRET_KEY = 'SUPER_SECRET'
    DEBUG = True
    TESTING = False
    SQLALCHEMY_DATABASE_URI= 'sqlite:///' + os.path.join(root_dir, 'app/schema.db').replace('\\', '/')
    ROOT_DIR = root_dir
    PROFILES_IMG_DIR = os.path.join(root_dir, 'app/static/images/profiles').replace('\\', '/')
    PROFILES_IMG_DEFAULT_DIR = os.path.join(root_dir, 'app/static/images/res').replace('\\', '/')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevConfig(DefaultConfig):
    DEBUG = True
    TESTING = True

class TestConfig(DefaultConfig):
	TESTING = True

class ProdConfig(DefaultConfig):
    DEBUG = False
    TESTING = False