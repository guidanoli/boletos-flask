import os
from datetime import datetime

from flask import Blueprint, render_template, request, redirect, url_for, current_app, flash

from app.upload import get_upload_path, send_upload, generate_filename, remove_upload, get_extension
from app.db import get_db, get_service, get_payment

bp = Blueprint('payment', __name__)

ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif'}


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
            except db.IntegrityError as e:
                error = e
            else:
                return redirect(url_for('service.index', service_id=service_id))

        flash(error)

    kwargs = {}
    kwargs['service'] = service
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
    return send_upload(payment['filename'])


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
        except db.IntegrityError as e:
            error = e
        else:
            remove_upload(payment['filename'])
            return redirect(url_for('service.index', service_id=service_id))

        flash(error)

    kwargs = {}
    kwargs['service'] = service
    kwargs['payment'] = payment
    return render_template('service/payment/delete.html', **kwargs)
