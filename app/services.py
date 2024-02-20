import flask

bp = flask.Blueprint('services', __name__, url_prefix='/services')


@bp.route('/new')
def new():
    return flask.render_template('services/new.html')
