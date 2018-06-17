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


def initDescriptions(C):
    from websrc.utils import getHtmlElement
    q_db = getDataBase()
    local_dir = C["local_dir"]
    target_dir = C["target_dir"]
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
            styles = """
            body {
                background-color: cyan;
            }
            code {
                background-color: orange;
                color: darkblue;
                white-space: pre;
                font-family: fantasy;
            }
            h2 {
                color: darkblue;
            }
            """
            with open(target_dir + "/" + f + "/index.html", "w") as fout:
                html = getHtmlElement(tag="h2", msg=f, selfclose=False)
                html += markdown(md)
                template_file = C['templates'] + "/index.html"
                ftemp = open(template_file, 'r')
                template = Template(ftemp.read())
                ftemp.close()
                fout.write(template.render(
                    styles=styles,
                    page_body=html))
            os.chmod(target_dir + "/" + f + "/index.html", 0o777)
            click.echo("Deployed description of " + f + " into webpage!")
        except:
            click.echo("Warning: Deploying description for " + f + " failed!")



def dumpDatabase(C):
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
                click.echo("Dumping " + q_title + " failed!. Please do it manually!")


def dumpDescription(C, q_id):
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
        click.echo("Dumping " + q_data["title"] + " failed!. Please do it manually!")


def deployDescription(C, q_id):
    from websrc.utils import getHtmlElement
    q_db = getDataBase()
    target_dir = C["target_dir"]
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
        styles = """
            body {
                background-color: white;
            }
            code {
                background-color: orange;
                color: darkblue;
                white-space: pre;
                font-family: fantasy;
            }
            h2 {
                color: darkblue;
            }
        """
        with open(q_dir + "/index.html", "w") as fout:
            html = getHtmlElement(tag="h2", msg=q_data["title"], selfclose=False)
            html += markdown(q_data["description"])
            template_file = C['templates'] + "/index.html"
            ftemp = open(template_file, 'r')
            template = Template(ftemp.read())
            ftemp.close()
            fout.write(template.render(
                styles=styles,
                page_body=html))
        os.chmod(q_dir + "/index.html", 0o777)
        click.echo("Deploying succeed!")
    except:
        click.echo("Deploying description for " + q_data["title"] + " failed!")


@click.command('init-database')
@with_appcontext
def initDataBaseCommand():
    initDataBase()
    initDescriptions(C)
    click.echo("Initialized the database!!")


@click.command('dump-database')
@with_appcontext
def dumpDataBaseCommand():
    dumpDatabase(C)
    click.echo("Finish dumping database!!")


@click.command('dump-description')
@click.option('--qid', help='question id', default='1')
@with_appcontext
def dumpDescriptionCommand(qid):
    dumpDescription(C, qid)


@click.command('deploy-description')
@click.option('--qid', help='question id', default='1')
@with_appcontext
def deployDescriptionCommand(qid):
    deployDescription(C, qid)



def initApp():
    app.teardown_appcontext(closeDataBase)
    app.cli.add_command(initDataBaseCommand)
    app.cli.add_command(dumpDataBaseCommand)
    app.cli.add_command(dumpDescriptionCommand)
    app.cli.add_command(deployDescriptionCommand)