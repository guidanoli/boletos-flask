import flask

from . import payment

bp = flask.Blueprint('service', __name__, url_prefix='/service')

bp.register_blueprint(payment.bp)

@bp.route('/new')
def new():
    return flask.render_template('service/new.html')
