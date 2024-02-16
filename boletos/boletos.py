import os
import uuid
from datetime import datetime

from flask import Blueprint, request, current_app, redirect, url_for, flash, render_template

from werkzeug.utils import secure_filename

from boletos.db import get_db
from boletos.service import get_service
from boletos.errors import FlashMessage

ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif'}

bp = Blueprint('boletos', __name__, url_prefix='/boletos')


def get_extension(filename):
    if '.' in filename:
        return filename.rsplit('.', 1)[1].lower()


def check_file():
    if 'file' not in request.files:
        raise FlashMessage('O arquivo do boleto é obrigatório.')
    return request.files['file']


def check_filename(filename):
    if not filename:
        raise FlashMessage('O arquivo do boleto é obrigatório.')
    else:
        ext = get_extension(filename)
        if ext not in ALLOWED_EXTENSIONS:
            raise FlashMessage('O arquivo do boleto deve ser um PDF ou uma imagem.')
        else:
            while True:
                filename = str(uuid.uuid4()) + '.' + ext
                filepath = os.path.join(current_app.config['UPLOADS_DIR'], filename)
                if not os.path.exists(filepath):
                    return filename, filepath

def check_amount(amount):
    if not amount:
        raise FlashMessage('O valor do boleto é obrigatório.')
    try:
        amount = round(float(amount), 2)
    except ValueError:
        raise FlashMessage('O valor do boleto deve ser um número decimal.')
    else:
        if amount >= 0:
            return amount
        else:
            raise FlashMessage('O valor do boleto deve ser um número decimal positivo.')


def check_ts(ts, datename):
    if not ts:
        raise FlashMessage(f'A data de {datename} é obrigatória.')
    try:
        return int(datetime.fromisoformat(ts).timestamp())
    except (ValueError, OverflowError, OSError):
        raise FlashMessage(f'A data de {datename} deve ser válida.')


def register_boleto(service_id, filename, amount, expiry_ts):
    try:
        db = get_db()
        db.execute(
            '''
            INSERT INTO boleto (service_id, filename, amount, expiry_ts)
            VALUES (?, ?, ?, ?)
            ''',
            (service_id, filename, amount, expiry_ts)
        )
        db.commit()
    except db.IntegrityError:
        raise FlashMessage('Erro ao registrar boleto no banco de dados.')


def _register(service_id):
    file = check_file()
    filename, filepath = check_filename(file.filename)
    amount = check_amount(request.form['amount'])
    expiry_ts = check_ts(request.form['expiry_ts'], 'vencimento')
    register_boleto(service_id, filename, amount, expiry_ts)
    file.save(filepath)


@bp.route('/register/<int:service_id>', methods=('GET', 'POST'))
def register(service_id):
    if request.method == 'POST':
        try:
            _register(service_id)
        except FlashMessage as e:
            flash(*e.args)
        else:
            return redirect(url_for('index'))

    service = get_service(service_id)
    return render_template('boletos/register.html', service=service)
