import operator
from datetime import datetime
import sqlite3

from flask import current_app, g, abort


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
        g.db.execute('PRAGMA foreign_keys = ON')

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_app(app):
    app.teardown_appcontext(close_db)


def get_services():
    db = get_db()
    now = datetime.now()
    services = db.execute(
        '''
        SELECT *, service_id IN
        (SELECT s.service_id
        FROM payment p JOIN service s
        ON p.service_id = s.service_id
        WHERE (frequency = 'y' AND year = ?)
        OR (frequency = 'm' AND year = ? AND month = ?)) AS paid
        FROM service
        ORDER BY name
        ''',
        (now.year, now.year, now.month)
    ).fetchall()

    return services


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
        ORDER BY year DESC, month DESC, day DESC
        ''',
        (service_id, )
    ).fetchall()

    return payments


def get_last_payments_for(service_id):
    """Returns None if service has no payments"""
    db = get_db()
    payments = db.execute(
        '''
        SELECT *
        FROM payment
        WHERE service_id = ?
        ORDER BY year DESC, month DESC, day DESC
        LIMIT 6
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


def get_service_images():
    db = get_db()
    images = db.execute(
        '''
        SELECT image
        FROM service
        WHERE image IS NOT NULL
        '''
    ).fetchall()

    return list(map(operator.itemgetter('image'), images))


def get_payment_files():
    db = get_db()
    files = db.execute(
        '''
        SELECT filename
        FROM payment
        WHERE filename IS NOT NULL
        '''
    ).fetchall()

    return list(map(operator.itemgetter('filename'), files))


def get_uploads():
    return get_service_images() + get_payment_files()
