import os
from . import app
from .config import TestConfig, ProdConfig
from .database import initApp
from . import auth
from . import question
from . import solution

app.config.from_object(TestConfig)

if not os.path.exists(app.instance_path):
    os.makedirs(app.instance_path)

initApp()

app.register_blueprint(auth.blueprint)
app.register_blueprint(question.blueprint)
app.register_blueprint(solution.blueprint)
app.add_url_rule("/", endpoint='index')

@app.route('/config')
def getConfig():
    return str(dict(app.config))

@app.route('/index')
def index():
    return "Succeed!!!"