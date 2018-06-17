import functools
from markdown2 import markdown
from .database import getDataBase
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from .auth import loginRequired
from .database import getDataBase
from .question import getQData

blueprint = Blueprint('solution', __name__, url_prefix='/solution')


def getSingleSolution(s_id):
    return getDataBase().execute(
        "SELECT * FROM solution WHERE solution_id = ?", (str(s_id), )
    ).fetchone()


@blueprint.route("/solution", methods=('GET', 'POST'))
@loginRequired
def showSolution():
    s_id = request.args.get("s_id", type=str)
    s_data = getSingleSolution(s_id)
    q_data = getDataBase().execute(
        "SELECT * FROM question WHERE id = ?", (str(s_data['question_id']))).fetchone()
    if not q_data:
        flash("Something is wrong, did not find the question from database!")
    return render_template(
        'solution/spage.html', Q=q_data, S=s_data,
        S_des=markdown(s_data["interpretation"]))


@blueprint.route("/screate", methods=('GET', 'POST'))
@loginRequired
def createSolution():
    q_title = request.args.get("q_title", type=str)
    q_data = getQData(q_title)
    if request.method == 'POST':
        database = getDataBase()
        s_data = database.execute(
            'SELECT * FROM solution WHERE question_id = ? AND nickname = ?',
            (q_data["id"], request.form['nickname'])
        ).fetchone()
        if s_data:
            flash("Solution " + request.form['nickname'] + "for the question already exists!")
            return render_template(
                'solution/screate.html', Q=q_data)
        else:
            database.execute(
                'INSERT INTO solution (author_id, question_id, author, language, nickname, interpretation, sourcecode)'
                ' VALUES (?, ?, ?, ?, ?, ?, ?)', (
                    g.user['id'], q_data['id'], g.user['username'], request.form['language'],
                    request.form['nickname'], request.form['interpretation'], request.form['sourcecode']
                )
            )
            database.commit()
        return redirect(url_for('question.showQuestion', q_title=q_title))
    return render_template(
        'solution/screate.html', Q=q_data)


@blueprint.route("/editcode", methods=('GET', 'POST'))
@loginRequired
def editCode():
    s_id = request.args.get("s_id", type=str)
    s_data = getSingleSolution(s_id)
    q_data = getDataBase().execute(
        "SELECT * FROM question WHERE id = ?", (str(s_data['question_id']))).fetchone()
    if not q_data:
        flash("Something is wrong, did not find the question from database!")
    if request.method == 'POST':
        database = getDataBase()
        database.execute(
            'UPDATE solution SET language = ?, sourcecode = ?'
            ' WHERE solution_id = ?', (request.form['language'], request.form['sourcecode'], s_data['solution_id'])
        )
        database.commit()
        return redirect(url_for('solution.showSolution', s_id=s_id))
    return render_template(
        'solution/editcode.html', Q=q_data, S=s_data,
        S_des=markdown(s_data["interpretation"]))


@blueprint.route("/editinter", methods=('GET', 'POST'))
@loginRequired
def editInter():
    s_id = request.args.get("s_id", type=str)
    s_data = getSingleSolution(s_id)
    q_data = getDataBase().execute(
        "SELECT * FROM question WHERE id = ?", (str(s_data['question_id']))).fetchone()
    if not q_data:
        flash("Something is wrong, did not find the question from database!")
    if request.method == 'POST':
        database = getDataBase()
        database.execute(
            'UPDATE solution SET nickname = ?, interpretation = ?'
            ' WHERE solution_id = ?', (request.form['nickname'], request.form['interpretation'], s_data['solution_id'])
        )
        database.commit()
        return redirect(url_for('solution.showSolution', s_id=s_id))
    return render_template(
        'solution/editinter.html', Q=q_data, S=s_data)

