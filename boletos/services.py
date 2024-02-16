from flask import Blueprint, request, redirect, url_for, flash, render_template

from boletos.db import get_db

bp = Blueprint('services', __name__, url_prefix='/services')

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
