import sqlite3

import click
from flask import current_app, g, abort


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


def get_service(service_id):
    db = get_db()
    service = db.execute(
        '''
        SELECT *
        FROM service
        WHERE service_id = ?
        ''',
        (service_id, )
    ).fetchone()

    if service is None:
        abort(404)

    return service


def get_payments_for(service_id):
    db = get_db()
    payments = db.execute(
        '''
        SELECT *
        FROM payment
        WHERE service_id = ?
        ORDER BY year DESC, month DESC
        ''',
        (service_id, )
    ).fetchall()

    return payments


def get_payment(service_id, year, month):
    db = get_db()
    payment = db.execute(
        '''
        SELECT *
        FROM payment
        WHERE service_id = ?
        AND year = ?
        AND month = ?
        ''',
        (service_id, year, month)
    ).fetchone()

    if payment is None:
        abort(404)

    return payment
