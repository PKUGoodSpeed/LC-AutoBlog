import json
SETUP_CFG = json.load(open('./configs/setup.json', 'r'))

from flask import Flask
app = Flask(__name__, instance_relative_config=True)
from . import autobase