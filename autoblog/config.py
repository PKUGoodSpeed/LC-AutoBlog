from . import app


class BaseConfig:
    DEBUG = True
    DEVELOPMENT = True


class TestConfig(BaseConfig):
    SECRET_KEY = "auto_blog"
    DATABASE = app.instance_path + '/test.database'


class ProdConfig(BaseConfig):
    SECRET_KEY = "are-you-fucking-retarded"
    DATABASE = app.instance_path + '/prod.database'