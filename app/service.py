from flask import Blueprint, request, render_template, redirect, flash, url_for, abort

from . import payment
from app.db import get_db, get_service, get_payments_for

bp = Blueprint('service', __name__, url_prefix='/service')

bp.register_blueprint(payment.bp)

@bp.route('/new', methods=('GET', 'POST'))
def new():
    if request.method == 'POST':
        name = request.form.get('name')
        frequency = request.form.get('frequency')
        db = get_db()
        error = None

        if not name:
            error = 'A name is required.'
        elif not frequency:
            error = 'A frequency is required.'

        if error is None:
            try:
                db.execute(
                    '''
                    INSERT INTO service (name, frequency)
                    VALUES (?, ?)
                    ''',
                    (name, frequency)
                )
                db.commit()
            except db.IntegrityError as e:
                error = e
            else:
                return redirect(url_for('index'))

        flash(error)

    kwargs = {}
    kwargs['frequencies'] = ('m', 'y')
    return render_template('service/new.html', **kwargs)


@bp.route('/<int:service_id>')
def index(service_id):
    service = get_service(service_id)
    payments = get_payments_for(service_id)
    kwargs = {}
    kwargs['service'] = service
    kwargs['payments'] = payments
    return render_template('service/index.html', **kwargs)


@bp.route('/<int:service_id>/delete', methods=('GET', 'POST'))
def delete(service_id):
    service = get_service(service_id)

    if request.method == 'POST':
        error = None

        db = get_db()
        try:
            db.execute(
                '''
                DELETE FROM service
                WHERE service_id = ?
                ''',
                (service_id, )
            )
            db.commit()
        except db.IntegrityError as e:
            error = e
        else:
            return redirect(url_for('index'))

        flash(error)

    kwargs = {}
    kwargs['service'] = service
    return render_template('service/delete.html', **kwargs)


@bp.route('/<int:service_id>/set-active/<int:active>')
def set_active(service_id, active):
    service = get_service(service_id)
    db = get_db()
    try:
        db.execute(
            '''
            UPDATE service
            SET active = ?
            WHERE service_id = ?
            ''',
            (active, service_id)
        )
        db.commit()
    except db.IntegrityError as e:
        flash(e)

    return redirect(url_for('service.index', service_id=service_id))
