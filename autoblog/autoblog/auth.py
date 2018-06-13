import functools
from .database import getDataBase
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

blueprint = Blueprint('auth', __name__, url_prefix='/auth')

# The first view: register
@blueprint.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        verify_password = request.form["verify_password"]
        email = request.form["email"]
        security = request.form["security"]
        usr_db = getDataBase()
        error = None

        if not username:
            error = "Username is required!"
        elif not password:
            error = "Password is required!"
        elif password != verify_password:
            error = "Come on! Just type your password twice! You can do it!"
        elif email.split('.')[-1] != 'edu':
            error = "Haven't you attend university!? Use your university email!"
        elif usr_db.execute(
            "SELECT id FROM author where username = ?", (username, )
        ).fetchone() is not None:
            error = "This guy {} is already registered! You must be a fake one!".format(username)
        elif security.lower() != "chaoran":
            error = "You should use your feet to think, which make things better!"

        if not error:
            usr_db.execute(
                "INSERT INTO author (username, password, email) VALUES (?, ?, ?)", (
                    username, generate_password_hash(password), email)
            )
            usr_db.commit()
            return redirect(url_for('auth.login'))
        flash(error)
    return render_template('auth/register.html')

# The second view: login
@blueprint.route("/login", methods=('GET', 'POST'))
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        usr_db = getDataBase()
        error = None

        user = usr_db.execute(
            "SELECT * FROM author WHERE username = ?", (username, )
        ).fetchone()

        if not user:
            error = "People who cannot remember their usernames are definitely idiots!"
        elif not check_password_hash(user["password"], password):
            error = "People who cannot remember their passwords are definitely idiots!"

        if not error:
            session.clear()
            session['user_id'] = user["id"]
            return redirect(url_for('index'))

        flash(error)
    return render_template('auth/login.html')

# handle logged in users
@blueprint.before_app_request
def loadLoggedInUser():
    user_id = session.get('user_id')

    if not user_id:
        g.user = None
    else:
        g.user = getDataBase().execute(
            "SELECT * FROM author WHERE id = ?", (user_id, )).fetchone()


# Logout
@blueprint.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


# Authentication views
def loginRequired(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view
