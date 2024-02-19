import os
import uuid
from datetime import datetime

from flask import abort, Blueprint, request, current_app, redirect, url_for, flash, render_template, send_from_directory

from werkzeug.utils import secure_filename

from boletos.db import get_db, get_service, get_boleto
from boletos.errors import FlashMessage
import boletos.utils as u

ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif'}

bp = Blueprint('boletos', __name__, url_prefix='/boletos')


@bp.route('/<int:boleto_id>')
def index(boleto_id):
    boleto = get_boleto(boleto_id)

    if not boleto:
        abort(404)

    service = get_service(boleto['service_id'])

    if not service:
        abort(404)

    kwargs = {}
    kwargs['boleto'] = boleto
    kwargs['service'] = service
    kwargs['u'] = u
    return render_template('boletos/index.html', **kwargs)


def check_file():
    if 'file' not in request.files:
        raise FlashMessage('O arquivo do boleto é obrigatório.')
    return request.files['file']


def check_filename(filename):
    if not filename:
        raise FlashMessage('O arquivo do boleto é obrigatório.')
    else:
        ext = u.get_extension(filename)
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


def register_boleto(service_id, filename, amount, expiry_ts, paid):
    try:
        db = get_db()
        db.execute(
            '''
            INSERT INTO boleto (service_id, filename, amount, expiry_ts, paid)
            VALUES (?, ?, ?, ?, ?)
            ''',
            (service_id, filename, amount, expiry_ts, paid)
        )
        db.commit()
    except db.IntegrityError:
        raise FlashMessage('Erro ao registrar boleto no banco de dados.')


def _register(service_id):
    file = check_file()
    filename, filepath = check_filename(file.filename)
    amount = check_amount(request.form['amount'])
    expiry_ts = check_ts(request.form['expiry_ts'], 'vencimento')
    paid = request.form.get('paid') is not None
    register_boleto(service_id, filename, amount, expiry_ts, paid)
    file.save(filepath)


@bp.route('/new/<int:service_id>', methods=('GET', 'POST'))
def register(service_id):

    service = get_service(service_id)

    if not service:
        abort(404)

    if request.method == 'POST':
        try:
            _register(service_id)
        except FlashMessage as e:
            flash(*e.args)
        else:
            return redirect(url_for('services.index', service_id=service_id))

    return render_template('boletos/register.html', service=service)


@bp.route('/<int:boleto_id>/view')
def view(boleto_id):
    boleto = get_boleto(boleto_id)

    if not boleto:
        abort(404)

    return send_from_directory(current_app.config['UPLOADS_DIR'], boleto['filename'])


def set_paid(boleto_id, paid, idempotent_error):
    boleto = get_boleto(boleto_id)

    if not boleto:
        abort(404)

    error = None

    if boleto['paid'] == paid:
        error = idempotent_error
    else:
        db = get_db()
        try:
            db.execute(
                '''
                UPDATE boleto
                SET paid = ?
                WHERE id = ?
                ''',
                (paid, boleto_id)
            )
            db.commit()
        except db.IntegrityError:
            error = 'Erro ao atualizar boleto no banco de dados.'

    if error:
        flash(error)

    return redirect(url_for('services.index', service_id=boleto['service_id']))


@bp.route('/<int:boleto_id>/pay')
def pay(boleto_id):
    return set_paid(boleto_id, 1, 'Este boleto já foi pago.')


@bp.route('/<int:boleto_id>/unpay')
def unpay(boleto_id):
    return set_paid(boleto_id, 0, 'Este boleto não foi pago ainda.')


@bp.route('/<int:boleto_id>/delete')
def delete(boleto_id):
    boleto = get_boleto(boleto_id)

    if not boleto:
        abort(404)

    error = None

    db = get_db()
    try:
        db.execute(
            '''
            DELETE FROM boleto
            WHERE id = ?
            ''',
            (boleto_id,)
        )
        db.commit()
        os.remove(os.path.join(current_app.config['UPLOADS_DIR'], boleto['filename']))
    except db.IntegrityError:
        error = 'Erro ao remover boleto do banco de dados.'

    if error:
        flash(error)

    return redirect(url_for('services.index', service_id=boleto['service_id']))
