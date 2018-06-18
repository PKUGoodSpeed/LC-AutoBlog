"""
Flask Server
@author: pkugoodspeed
@date: 06/12/2018
@copyright: jogchat.com
"""
import os
from flask import render_template
from . import app
from .config import TestConfig, ProdConfig
from .database import initApp
from . import auth
from . import question
from . import solution

# app.config.from_object(TestConfig)
app.config.from_object(ProdConfig)


if not os.path.exists(app.instance_path):
    os.makedirs(app.instance_path)

initApp()

app.register_blueprint(auth.blueprint)
app.register_blueprint(question.blueprint)
app.register_blueprint(solution.blueprint)
# app.add_url_rule("/", endpoint='qustion.index')

@app.route('/config')
def getConfig():
    return str(dict(app.config))

