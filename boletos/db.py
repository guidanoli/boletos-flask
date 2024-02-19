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
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


def get_services():
    return get_db().execute(
            '''
            SELECT *
            FROM service
            LEFT JOIN (SELECT service_id, MAX(expiry_ts) AS max_paid_expiry_ts
                       FROM boleto
                       WHERE paid = 1
                       GROUP BY service_id
                       ORDER BY expiry_ts DESC) ON service.id = service_id
            ORDER BY max_paid_expiry_ts ASC
            '''
    ).fetchall()


def get_service(service_id):
    return get_db().execute('SELECT * FROM service WHERE id = ?', (service_id,)).fetchone()


def get_boleto(boleto_id):
    return get_db().execute('SELECT * FROM boleto WHERE id = ?', (boleto_id,)).fetchone()


def get_boletos_from(service_id):
    return get_db().execute('SELECT * FROM boleto b WHERE b.service_id = ? ORDER BY b.expiry_ts DESC', (service_id,)).fetchall()
