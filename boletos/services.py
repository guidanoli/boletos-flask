from datetime import datetime

from flask import Blueprint, request, redirect, url_for, flash, render_template

from boletos.db import get_db, get_service, get_boletos

bp = Blueprint('services', __name__, url_prefix='/services')


@bp.route('/<int:service_id>')
def index(service_id):
    service = get_service(service_id)
    boletos = get_boletos(service_id)
    kwargs = {}
    kwargs['service'] = service
    kwargs['boletos'] = boletos
    kwargs['fmtdate'] = (lambda ts: datetime.fromtimestamp(ts).strftime('%d/%m/%Y'))
    kwargs['fmttime'] = (lambda ts: datetime.fromtimestamp(ts).strftime('%Hh%M'))
    kwargs['fmtamount'] = (lambda a: 'R$ {:.2f}'.format(a))
    kwargs['curr_ts'] = datetime.now().timestamp()
    return render_template('services/index.html', **kwargs)


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        name = request.form['name']
        db = get_db()
        error = None

        if not name:
            error = 'O nome do serviço é obrigatório.'

        if error is None:
            try:
                db.execute(
                    'INSERT INTO service (name) VALUES (?)',
                    (name,)
                )
                db.commit()
            except db.IntegrityError:
                error = 'Um serviço com esse nome já existe.'
            else:
                return redirect(url_for('index'))

        flash(error)

    return render_template('services/register.html')
