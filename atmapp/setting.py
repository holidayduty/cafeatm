import functools
from flask import(
    Blueprint, flash, g, request, render_template, redirect, url_for
)
from werkzeug.exceptions import abort
from .db import get_db

bp = Blueprint('setting', __name__, '/')


@bp.route('/edit', methods=('POST', 'GET'))
# userはsqlから探す?
def edit():
    if request.method == 'POST':
        sex = request.form.getlist('sexes')
        birth_date = request.date
        user_profile = request.form('profile')
        error = None
