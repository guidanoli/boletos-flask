import os
import uuid
from datetime import datetime
import calendar

from flask import Blueprint, render_template, request, redirect, url_for, current_app

from app.db import get_db, get_service

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
        assert ext in ALLOWED_EXTENSIONS

        filename, filepath = generate_filename(ext)
        file.save(filepath)

        if error is None:
            db = get_db()
            db.execute(
                '''
                INSERT INTO payment (service_id, filename, year, month)
                VALUES (?, ?, ?, ?)
                ''',
                (service_id, filename, year, month)
            )
            db.commit()
            return redirect(url_for('service.index', service_id=service_id))

        flash(error)

    kwargs = {}
    kwargs['service'] = service
    kwargs['months'] = enumerate(calendar.month_name[1:], start=1)
    kwargs['now'] = datetime.now()
    return render_template('service/payment/new.html', **kwargs)
