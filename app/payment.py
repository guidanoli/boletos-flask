import flask

bp = flask.Blueprint('payment', __name__)


@bp.route('/<int:service_id>/payment/new')
def new():
    return flask.render_template('service/payment/new.html')
