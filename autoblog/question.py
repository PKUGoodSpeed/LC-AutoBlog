from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session)
from werkzeug.exceptions import abort
from .auth import loginRequired
from .database import getDataBase
import websrc.index as windex
from websrc.utils import getHtmlElement

blueprint = Blueprint('question', __name__)

@blueprint.route("/qindex")
@loginRequired
def index():
    database = getDataBase()
    questions = database.execute(
        'SELECT title FROM question').fetchall()
    folders = [q["title"] for q in questions]
    addr = "http://" + request.host + "/question?qdisplay="
    styles = windex.getIndexStyle(theme="cyan")
    page_body = getHtmlElement(tag='h4', msg="editor mode", selfclose=False, style="\"color:magenta\"")
    page_body += windex.getIndexBodyFromList(folders, addr)
    page_scripts = windex.getSearchScripts()
    return render_template(
        'question/index.html',
        styles=styles,
        page_body=page_body,
        page_scripts=page_scripts)

