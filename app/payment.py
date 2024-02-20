import flask

bp = flask.Blueprint('payment', __name__, url_prefix='/payment')


@bp.route('/new')
def new():
    return flask.render_template('payment/new.html')
