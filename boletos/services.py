from datetime import datetime

from flask import Blueprint, request, redirect, url_for, flash, render_template

from boletos.db import get_db, get_service, get_boletos_from
import boletos.utils as u

bp = Blueprint('services', __name__, url_prefix='/services')


@bp.route('/<int:service_id>')
def index(service_id):
    service = get_service(service_id)
    boletos = get_boletos_from(service_id)
    kwargs = {}
    kwargs['service'] = service
    kwargs['boletos'] = boletos
    kwargs['u'] = u
    kwargs['curr_ts'] = datetime.now().timestamp()
    return render_template('services/index.html', **kwargs)


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        frequency = request.form.get('frequency')
        db = get_db()
        error = None

        if not name:
            error = 'O nome do serviço é obrigatório.'
        elif not frequency:
            error = 'A frequência de cobrança é obrigatória.'
        elif frequency not in ('monthly', 'yearly'):
            error = 'A frequência de cobrança deve ser mensal ou anual.'

        if error is None:
            try:
                db.execute(
                    'INSERT INTO service (name, frequency) VALUES (?, ?)',
                    (name, frequency)
                )
                db.commit()
            except db.IntegrityError:
                error = 'Um serviço com esse nome já existe.'
            else:
                return redirect(url_for('index'))

        flash(error)

    return render_template('services/register.html')
