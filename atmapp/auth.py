import functools
from flask import(
    Blueprint, flash, g, request, render_template, redirect, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from .db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('POST', 'GET'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

    if not username:
        error = 'Username is required.'
    elif not password:
        error = 'Password is required.'
    elif db.execute(
        'SELECT id FROM user WHERE username=?', (username,)
    ).fetchone() is not None:
        error = 'Username {} is already registered. '.format(username)

    if error is None:
        db.execute(
            'INSERT INTO user(username, password) VALUES(?, ?)',
            (username, generate_password_hash(password))
        )
        db.commit()
        return redirect(url_for('auth.login'))

        flash(error)
    return render_template('auth/register.html')


@dp.route('/login', methods=('GET', 'POST'))
def login():
    if request.form == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

    if user is None:
        error = 'Incorrect username.'
    elif not check_password_hash(user['password'], password):
        error = 'Incorrect password'

    if error is None:
        session.clear()
        session['user_id'] = user['id']
        return redirect(url_for('top'))

        flash(error)
    return render_template('auth/login.html')


@bp.before_app_request(f)
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))


def login_required():
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view()
