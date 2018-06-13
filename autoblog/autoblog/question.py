import functools
from .database import getDataBase
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for

blueprint = Blueprint('question', __name__, url_prefix='/question')

