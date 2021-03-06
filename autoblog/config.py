"""
Flask Server
@author: pkugoodspeed
@date: 06/12/2018
@copyright: jogchat.com
"""
from . import app


class BaseConfig:
    DEBUG = True
    DEVELOPMENT = True


class TestConfig(BaseConfig):
    SECRET_KEY = "auto_blog"
    DATABASE = app.instance_path + '/test.database'


class ProdConfig(BaseConfig):
    SECRET_KEY = "are-you-fucking-retarded"
    DATABASE = app.instance_path + '/jogchat_leetcode.database'