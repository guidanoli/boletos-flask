import sqlite3

import click
from flask import current_app, g


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()
    for filepath in ('schema.sql', 'views.sql'):
        with current_app.open_resource(filepath) as f:
            db.executescript(f.read().decode('utf8'))


@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


def get_service(service_id):
    return get_db().execute('SELECT * FROM service s WHERE s.id = ?', (service_id,)).fetchone()


def get_boletos(service_id):
    return get_db().execute('SELECT * FROM boleto b WHERE b.service_id = ? ORDER BY b.expiry_ts DESC', (service_id,)).fetchall()


def get_boleto(service_id, boleto_id):
    return get_db().execute('SELECT * FROM boleto b WHERE b.service_id = ? AND b.id = ?', (service_id, boleto_id)).fetchone()


def get_services():
    return get_db().execute('''
        SELECT id, name, last_payment_ts
        FROM service
        LEFT OUTER JOIN (SELECT service_id, MAX(payment_ts) as last_payment_ts
                         FROM boleto
                         GROUP BY service_id)
        ON id = service_id
        ORDER BY last_payment_ts
 ''').fetchall()
