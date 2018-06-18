"""
Flask Server
@author: pkugoodspeed
@date: 06/12/2018
@copyright: jogchat.com
"""
import os
import sqlite3
from markdown2 import markdown
from jinja2 import Template
from datetime import datetime
from . import app
import click
from flask import g, render_template
from flask.cli import with_appcontext
from . import SETUP_CFG as C


def getDataBase():
    if "database" not in g:
        g.database = sqlite3.connect(
            app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.database.row_factory = sqlite3.Row
    return g.database


def setupQuestionTable(target_dir):
    database = getDataBase()
    


def closeDataBase(e=None):
    database = g.pop('database', None)
    if database is not None:
        database.close()


def initDataBase():
    database = getDataBase()
    with app.open_resource('schema.sql') as f:
        database.executescript(f.read().decode('utf8'))


def initDescriptions():
    from websrc.utils import getHtmlElement
    q_db = getDataBase()
    local_dir = C["local_dir"]
    target_dir = C["target_dir"]
    target_addr = C["target_web"]
    if not os.path.exists(local_dir):
        click.echo("local workspace is not setup!")
        return
    if not os.path.exists(target_dir):
        click.echo("target workspace is not setup")
        return
    for f in os.listdir(local_dir):
        if f[0] != '[':
            continue
        q_id = f[1:].split(']')[0]
        q = q_db.execute(
            "SELECT * FROM question WHERE id = ?", (q_id, )
        ).fetchone()
        if q:
            continue
        md = ""
        if os.path.exists(local_dir + "/" + f + "/README.md"):
            with open(local_dir + "/" + f + "/README.md", "r") as fin:
                md = fin.read()
        click.echo("Commit description of " + f + " into database!")
        try:
            # Save the md format of the description into database
            q_db.execute(
                "INSERT INTO question (id, title, description) VALUES (?, ?, ?)", (
                    q_id, f, md)
            )
            q_db.commit()
        except:
            click.echo("Warning: Initialized description for " + f + " failed!")

        try:
            styles = """body {background-color: white;font-family: Comic Sans MS;}
code {background-color: white;color: darkblue;white-space: pre;}
h2 {color: darkblue;}
#navi {list-style-type: none; margin: 0; padding: 0; overflow: hidden; background-color: #334;}
#navi li {float: left;}
#navi li a {display: block; color: white; text-align: center; padding: 14px 16px; text-decoration: none;}
#navi li div {display: block; color: white; text-align: center; padding: 14px 16px; text-decoration: none;}
#navi li a:hover {background-color: #111;}"""
            with open(target_dir + "/" + f + "/index.html", "w") as fout:
                html = getHtmlElement(tag="h2", msg=f, selfclose=False)
                html += markdown(md)
                template_file = C['templates'] + "/index.html"
                ftemp = open(template_file, 'r')
                template = Template(ftemp.read())
                ftemp.close()
                navs = [{'link': target_addr, "msg": "Index"}]
                fout.write(template.render(
                    styles=styles, page_body=html, NAVS=navs))
            os.chmod(target_dir + "/" + f + "/index.html", 0o777)
            click.echo("Deployed description of " + f + " into webpage!")
        except:
            click.echo("WARNGING: Deploying description for " + f + " failed!")



def dumpDatabase():
    q_db = getDataBase()
    local_dir = C["local_dir"]
    title_file = C["title_file"]
    click.echo("Dumping database to " + local_dir + " ...")
    if not os.path.exists(local_dir):
        os.makedirs(local_dir)
    with open(title_file, "r") as fin:
        for line in fin:
            q_title = line.replace("\n", "")
            q_dir = local_dir + "/" + q_title
            if not os.path.exists(q_dir):
                os.makedirs(q_dir)
            q_data = q_db.execute(
                "SELECT * FROM question WHERE title = ?", (q_title, )
            ).fetchone()
            if not q_data:
                click.echo(q_title + "does not exist in database!")
            try:
                with open(q_dir + "/README.md", "w") as fout:
                    fout.write(q_data["description"])
            except:
                click.echo("WARNGING: Dumping " + q_title + " failed!. Please do it manually!")


def dumpDescription(q_id):
    q_db = getDataBase()
    local_dir = C["local_dir"]
    click.echo("Dumping description for " + str(q_id) + " to " + local_dir + " ...")
    q_data = q_db.execute(
        "SELECT * FROM question WHERE id = ?", (q_id, )).fetchone()
    if not q_data:
        click.echo("Question " + str(q_id) + " does not exist in database!")
        return
    q_dir = local_dir + "/" + q_data["title"]
    if not os.path.exists(q_dir):
        os.makedirs(q_dir)
    try:
        with open(q_dir + "/README.md", "w") as fout:
            fout.write(q_data["description"])
        click.echo("Dumping succeed!")
    except:
        click.echo("WARNGING: Dumping " + q_data["title"] + " failed!. Please do it manually!")


def deployDescription(q_id):
    from websrc.utils import getHtmlElement
    q_db = getDataBase()
    target_dir = C["target_dir"]
    target_addr = C["target_web"]
    click.echo("Deploying description for " + str(q_id) + " to " + target_dir + " ...")
    q_data = q_db.execute(
        "SELECT * FROM question WHERE id = ?", (q_id, )).fetchone()
    if not q_data:
        click.echo("Question " + str(q_id) + " does not exist in database!")
        return
    q_dir = target_dir + "/" + q_data["title"]
    if not os.path.exists(q_dir):
        os.makedirs(q_dir)
    try:
        styles = """body {background-color: white;font-family: Comic Sans MS;}
code {background-color: white;color: darkblue;white-space: pre;}
h2 {color: darkblue;}
#navi {list-style-type: none; margin: 0; padding: 0; overflow: hidden; background-color: #334;}
#navi li {float: left;}
#navi li a {display: block; color: white; text-align: center; padding: 14px 16px; text-decoration: none;}
#navi li div {display: block; color: white; text-align: center; padding: 14px 16px; text-decoration: none;}
#navi li a:hover {background-color: #111;}"""
        with open(q_dir + "/index.html", "w") as fout:
            html = getHtmlElement(tag="h2", msg=q_data["title"], selfclose=False)
            html += markdown(q_data["description"])
            template_file = C['templates'] + "/index.html"
            ftemp = open(template_file, 'r')
            template = Template(ftemp.read())
            ftemp.close()
            navs = [{'link': target_addr, "msg": "Index"}]
            fout.write(template.render(
                styles=styles, page_body=html, NAVS=navs))
        os.chmod(q_dir + "/index.html", 0o777)
        click.echo("Deploying succeed!")
    except:
        click.echo("WARNGING: Deploying description for " + q_data["title"] + " failed!")


def _getSolutionMsg(s_data, q_data):
    msg = "=" * 50 + "\n"
    msg += "Solution id: " + str(s_data['solution_id']) + "\n"
    msg += "Question:    " + str(q_data['title']) + "\n"
    msg += "Nickname:    " + str(s_data['nickname']) + "\n"
    msg += "Author:      " + str(s_data["author"]) + "\n"
    msg += "Language:    " + str(s_data["language"]) + "\n"
    msg += "Complexity:  " + str(s_data["complexity"]) + "\n"
    msg += "Runtime:     " + str(s_data["runtime"]) + "\n"
    msg += "Percentage:  " + str(s_data["percentage"]) + "\n"
    msg += "-" * 50 + "\n"
    msg += "Go to {H}/{Q}/{S}.html to view solution details!\n".format(
        H=C['target_web'], Q=q_data['title'], S=s_data['nickname'])
    msg += "=" * 50 + "\n"
    return msg


def _getQuestionMsg(q_data):
    msg = "=" * 50 + "\n"
    msg += "Question:    " + str(q_data['title']) + "\n"
    msg += "-" * 50 + "\n"
    msg += "Description: \n"
    msg += str(q_data['description']) + "\n"
    msg += "-" * 50 + "\n"
    msg += "Go to {H}/{Q} to view question details\n".format(
        H=C['target_web'], Q=q_data['title'])
    msg += "=" * 50 + "\n"
    return msg


def checkQuestion(question_id):
    q_data = getDataBase().execute(
        "SELECT * FROM question WHERE id = ?", (str(question_id))).fetchone()
    if not q_data:
        click.echo("ERROR: Something is wrong, question#{ID} does not exists!".format(str(question_id)))
        return
    click.echo(_getQuestionMsg(q_data))


def checkSolution(solution_id):
    database = getDataBase()
    s_data = database.execute(
        'SELECT * FROM solution WHERE solution_id = ?', (str(solution_id))).fetchone()
    if not s_data:
        click.echo("ERROR: Solution with solution_id=" + str(solution_id) + " does not exist!")
        return
    q_data = database.execute(
        "SELECT * FROM question WHERE id = ?", (str(s_data['question_id']))).fetchone()
    if not q_data:
        click.echo("ERROR: Something is wrong, no question corresponds to this solution_id!!")
        return
    click.echo(_getSolutionMsg(s_data, q_data))


def deleteSolution(solution_id):
    database = getDataBase()
    s_data = database.execute(
        'SELECT * FROM solution WHERE solution_id = ?', (str(solution_id))).fetchone()
    if not s_data:
        click.echo("ERROR: Solution with solution_id=" + str(solution_id) + " does not exist!")
        return
    q_data = database.execute(
        "SELECT * FROM question WHERE id = ?", (str(s_data['question_id']))).fetchone()
    database.execute(
        'DELETE FROM solution WHERE solution_id = ?', (str(solution_id),))
    database.commit()
    solution_file = "/".join([C['target_dir'], q_data['title'], s_data['nickname'] + ".html"])
    os.remove(solution_file)
    msg = "Successfully delete solution id={ID}, nickname={NM}, author={AU}\n".format(
        ID=str(solution_id), NM=s_data['nickname'], AU=s_data['author'])
    click.echo("Succe")


@click.command('init-db')
@with_appcontext
def initDataBaseCommand():
    from shutil import copyfile
    # Make replica
    if os.path.exists(app.config["DATABASE"]):
        cache = C['db_cache']
        if not os.path.exists(cache):
            os.makedirs(cache)
        filename = cache + "/saved_"
        filename += str(datetime.now()).replace(" ", "_")
        filename += ".database"
        copyfile(app.config["DATABASE"], filename)
        click.echo("Old database is saved in " + filename)

    initDataBase()
    initDescriptions()
    click.echo("Initialized the database!!")


@click.command('save-db')
@with_appcontext
def saveDataBaseCommand():
    from shutil import copyfile
    # Make replica
    cache = C['db_cache']
    if not os.path.exists(cache):
        os.makedirs(cache)
    filename = cache + "/saved_"
    filename += str(datetime.now()).replace(" ", "_")
    filename += ".database"
    copyfile(app.config["DATABASE"], filename)
    click.echo("Database is saved in " + filename)


@click.command('dump-db')
@with_appcontext
def dumpDataBaseCommand():
    dumpDatabase()
    click.echo("Finish dumping database!!")


@click.command('dumpq')
@click.option('--qid', help='question id', default='1')
@with_appcontext
def dumpDescriptionCommand(qid):
    dumpDescription(qid)


@click.command('deplq')
@click.option('--qid', help='question id', default='1')
@with_appcontext
def deployDescriptionCommand(qid):
    deployDescription(qid)


@click.command('chq')
@click.option('--qid', help='question id', default='1')
@with_appcontext
def checkQuestionCommand(qid):
    checkQuestion(qid)


@click.command('chs')
@click.option('--sid', help='solution id', default='1')
@with_appcontext
def checkSolutionCommand(sid):
    checkSolution(sid)


@click.command('dels')
@click.option('--sid', help='solution id', default='1')
@with_appcontext
def deleteSolutionCommand(sid):
    deleteSolution(sid)


def initApp():
    app.teardown_appcontext(closeDataBase)
    app.cli.add_command(initDataBaseCommand)
    app.cli.add_command(saveDataBaseCommand)
    app.cli.add_command(dumpDataBaseCommand)
    app.cli.add_command(dumpDescriptionCommand)
    app.cli.add_command(deployDescriptionCommand)
    app.cli.add_command(checkQuestionCommand)
    app.cli.add_command(checkSolutionCommand)
    app.cli.add_command(deleteSolutionCommand)