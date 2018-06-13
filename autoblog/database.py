import os
import sqlite3
import markdown2
from . import app
import click
from flask import g, render_template
from flask.cli import with_appcontext


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
                background-color: grey;
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
                html += markdown2.markdown(md)
                fout.write(render_template(
                    'question/index.html', 
                    styles=styles,
                    page_body=html))
            os.chmod(target_dir + "/" + f + "/index.html", 0o777)
            click.echo("Deployed description of " + f + " into webpage!")
        except:
            click.echo("Warning: Deploying description for " + f + " failed!")


@click.command('init-database')
@click.option('--cfg', help='config file', default='./setup.json')
@with_appcontext
def initDataBaseCommand(cfg):
    if not os.path.exists(cfg):
        click.echo("Error: config file does not exist!")
    import json
    initDataBase()
    C = json.load(open(cfg, "r"))
    initDescriptions(C)
    click.echo("Initialized the database!!")

def initApp():
    app.teardown_appcontext(closeDataBase)
    app.cli.add_command(initDataBaseCommand)