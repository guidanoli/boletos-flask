import calendar
from datetime import datetime

from flask import Blueprint, render_template, request

import app.db as db

bp = Blueprint('index', __name__)


@bp.route('/')
def index():
    return render_template('index.html')


@bp.route('/due')
def due():
    return render_template(
        'table.html',
        title='Due payments',
        services=db.get_services_with_due_payment()
    )


@bp.route('/uptodate')
def uptodate():
    return render_template(
        'table.html',
        title='Up-to-date payments',
        services=db.get_services_with_uptodate_payment()
    )
