import flask
from flask import Blueprint, request, render_template, redirect, flash, url_for

from . import payment
from boletos.db import get_db

bp = Blueprint('service', __name__, url_prefix='/service')

bp.register_blueprint(payment.bp)

@bp.route('/new', methods=('GET', 'POST'))
def new():
    if request.method == 'POST':
        name = request.form.get('name')
        db = get_db()
        error = None

        if not name:
            error = 'A name is required.'

        if error is None:
            try:
                db.execute(
                    'INSERT INTO service (name) VALUES (?)',
                    (name, )
                )
                db.commit()
            except db.IntegrityError:
                error = 'A service with this name already exists.'
            else:
                return redirect(url_for('index'))

        flash(error)

    return render_template('service/new.html')


@bp.route('/<int:service_id>')
def index(service_id):
    return render_template('service/index.html')
