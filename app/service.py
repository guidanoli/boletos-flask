import calendar

from flask import Blueprint, request, render_template, redirect, flash, url_for, abort

from . import payment
from app.db import get_db, get_service, get_payments_for

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
                    '''
                    INSERT INTO service (name)
                    VALUES (?)
                    ''',
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
    service = get_service(service_id)
    payments = get_payments_for(service_id)
    kwargs = {}
    kwargs['service'] = service
    kwargs['payments'] = payments
    kwargs['month_name'] = calendar.month_name
    return render_template('service/index.html', **kwargs)
