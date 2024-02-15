from flask import Blueprint, request, redirect, url_for, flash, render_template

from boletos.db import get_db

bp = Blueprint('services', __name__, url_prefix='/services')

freq2str = {'M': 'Mensal', 'Y': 'Anual'}

@bp.route('/')
def index():
    db = get_db()
    services = db.execute(
        'SELECT name, freq FROM service'
        ' ORDER BY name'
    ).fetchall()
    return render_template('services/index.html', services=services, freq2str=freq2str)

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        name = request.form['name']
        freq = request.form['freq']
        db = get_db()
        error = None

        if not name:
            error = 'O nome do serviço é obrigatório.'
        elif not freq:
            error = 'A frequência de cobrança é obrigatória.'

        if freq not in ('M', 'Y'):
            error = 'A frequência de cobrança deve ser mensal ou anual.'

        if error is None:
            try:
                db.execute(
                    'INSERT INTO service (name, freq) VALUES (?, ?)',
                    (name, freq)
                )
                db.commit()
            except db.IntegrityError:
                error = 'Um serviço com esse nome já existe.'
            else:
                return redirect(url_for('services.index'))

        flash(error)

    return render_template('services/register.html')
