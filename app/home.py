import flask

from app.db import get_db

bp = flask.Blueprint('home', __name__)


@bp.route('/')
def index():
    db = get_db()
    services = db.execute('SELECT * FROM service').fetchall()
    kwargs = {}
    kwargs['services'] = services
    return flask.render_template('home.html', **kwargs)
