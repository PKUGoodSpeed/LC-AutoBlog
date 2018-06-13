import functools
from .database import getDataBase
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

blueprint = Blueprint('solution', __name__, url_prefix='/solution')
