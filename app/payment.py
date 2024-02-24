import os
import uuid
from datetime import datetime
import calendar

from flask import Blueprint, render_template, request, redirect, url_for, current_app, send_from_directory, flash

from app.db import get_db, get_service, get_payment

bp = Blueprint('payment', __name__)

ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif'}


def get_extension(filename):
    if '.' in filename:
        return filename.rsplit('.', 1)[1].lower()


def generate_filename(ext):
    while True:
        filename = str(uuid.uuid4()) + '.' + ext
        filepath = os.path.join(current_app.config['UPLOADS_DIR'], filename)
        if not os.path.exists(filepath):
            return filename, filepath


@bp.route('/<int:service_id>/payment/new', methods=('GET', 'POST'))
def new(service_id):
    service = get_service(service_id)

    if request.method == 'POST':
        error = None

        file = request.files['file']
        year = int(request.form['year'])
        month = int(request.form['month'])

        ext = get_extension(file.filename)
        if ext in ALLOWED_EXTENSIONS:
            filename, filepath = generate_filename(ext)
            file.save(filepath)
        else:
            error = 'Invalid file extension.'

        if error is None:
            db = get_db()
            try:
                db.execute(
                    '''
                    INSERT INTO payment (service_id, year, month, filename)
                    VALUES (?, ?, ?, ?)
                    ''',
                    (service_id, year, month, filename)
                )
                db.commit()
            except db.IntegrityError:
                error = 'A payment for this service and date already exist.'
            else:
                return redirect(url_for('service.index', service_id=service_id))

        flash(error)

    kwargs = {}
    kwargs['service'] = service
    kwargs['months'] = enumerate(calendar.month_name[1:], start=1)
    kwargs['now'] = datetime.now()
    return render_template('service/payment/new.html', **kwargs)


@bp.route('/<int:service_id>/payment/<int:year>/<int:month>')
def index(service_id, year, month):
    service = get_service(service_id)
    payment = get_payment(service_id, year, month)
    kwargs = {}
    kwargs['service'] = service
    kwargs['payment'] = payment
    return render_template('service/payment/index.html', **kwargs)


@bp.route('/<int:service_id>/payment/<int:year>/<int:month>/view')
def view(service_id, year, month):
    payment = get_payment(service_id, year, month)
    return send_from_directory(current_app.config['UPLOADS_DIR'], payment['filename'])


@bp.route('/<int:service_id>/payment/<int:year>/<int:month>/delete', methods=('GET', 'POST'))
def delete(service_id, year, month):
    service = get_service(service_id)
    payment = get_payment(service_id, year, month)

    if request.method == 'POST':
        error = None

        db = get_db()
        try:
            db.execute(
                '''
                DELETE FROM payment
                WHERE service_id = ?
                AND year = ?
                AND month = ?
                ''',
                (service_id, year, month)
            )
            db.commit()
        except db.IntegrityError:
            error = 'The server was unable to delete the payment from the database.'
        else:
            return redirect(url_for('service.index', service_id=service_id))

        flash(error)

    kwargs = {}
    kwargs['service'] = service
    kwargs['payment'] = payment
    return render_template('service/payment/delete.html', **kwargs)
