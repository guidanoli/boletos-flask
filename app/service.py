import flask

bp = flask.Blueprint('service', __name__, url_prefix='/service')


@bp.route('/new')
def new():
    return flask.render_template('service/new.html')
