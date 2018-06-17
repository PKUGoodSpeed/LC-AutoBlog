"""
Flask Server
@author: pkugoodspeed
@date: 06/12/2018
@copyright: jogchat.com
"""
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session)
from werkzeug.exceptions import abort
from .auth import loginRequired
from .database import getDataBase
import websrc.index as windex
from websrc.utils import getHtmlElement
from . import SETUP_CFG as C

blueprint = Blueprint('question', __name__)

def getSolutions(q_id):
    return getDataBase().execute(
        "SELECT * FROM solution WHERE question_id = ?", (q_id, )
    ).fetchall()

@blueprint.route("/qindex")
@loginRequired
def index():
    database = getDataBase()
    questions = database.execute(
        'SELECT title FROM question').fetchall()
    folders = [q["title"] for q in questions]
    addr = "http://" + request.host + "/question?q_title="
    styles = windex.getIndexStyle(theme="cyan")
    page_body = getHtmlElement(tag='h4', msg="editor mode", selfclose=False, style="\"color:magenta\"")
    page_body += windex.getIndexBodyFromList(folders, addr)
    page_scripts = windex.getSearchScripts()
    navs = []
    navs.append({"link": C["home_web"], "msg": "Prodhome"})
    navs.append({"link": C["target_web"], "msg": "Prodpage"})
    return render_template(
        'index.html',
        styles=styles,
        page_body=page_body,
        page_scripts=page_scripts,
        NAVS=navs)


def getQData(q_title):
    return getDataBase().execute(
        "SELECT * FROM question WHERE title = ?", (q_title, )
    ).fetchone()


def getQDescription(q_title):
    from markdown2 import markdown
    q_data = getQData(q_title)
    return markdown(q_data["description"])
    


@blueprint.route("/question", methods=('GET', 'POST'))
@loginRequired
def showQuestion():
    q_title = request.args.get("q_title", type=str)
    q_data = getQData(q_title)
    q_desc = getQDescription(q_title)
    solutions = getSolutions(q_data["id"])
    navs = []
    navs.append({"link": C["home_web"], "msg": "Prodhome"})
    navs.append({"link": url_for('question.index'), "msg": "Index"})
    navs.append({"link": C["target_web"] + "/" + q_data["title"], "msg": "Prodpage"})
    navs.append({"link": url_for('question.deployQuestion', q_title=q_title), "msg": "Deploy"})
    return render_template(
        'question/qpage.html',
        Q=q_data, Q_desc=q_desc, SOLUS=solutions,
        NAVS=navs)
 
 
@blueprint.route("/qedit", methods=('GET', 'POST'))
@loginRequired
def editQuestion():
    q_title = request.args.get("q_title", type=str)
    q_data = getQData(q_title)
    solutions = getSolutions(q_data['id'])

    if request.method == 'POST' and "q_desc" in request.form:
        q_desc = request.form["q_desc"]
        database = getDataBase()
        database.execute(
            'UPDATE question SET description = ? WHERE title = ?',
            (q_desc, q_title))
        database.commit()
        return redirect(url_for('question.showQuestion', q_title=q_title))
    navs = []
    navs.append({"link": C["home_web"], "msg": "Prodhome"})
    navs.append({"link": url_for('question.index'), "msg": "Index"})
    navs.append({"link": C["target_web"] + "/" + q_data["title"], "msg": "Prodpage"})
    return render_template(
        'question/qedit.html', Q=q_data, S=solutions,
        NAVS=navs)


 
@blueprint.route("/qdeploy", methods=('GET', 'POST'))
@loginRequired
def deployQuestion():
    from websrc.codeblock import getQuestionPage
    q_title = request.args.get("q_title", type=str)
    q_data = getQData(q_title)
    solutions = getSolutions(q_data['id'])
    question_dir = C['target_dir'] + "/" + q_title
    question_addr = C['target_web'] + "/" + q_title
    page_content = getQuestionPage(
        q_title, q_data["description"], solutions, C["templates"] + "/question.html", C["target_web"])
    with open(question_dir + "/index.html", "w") as fout:
        fout.write(page_content)
    return redirect(question_addr)
     

