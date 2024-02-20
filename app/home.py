import flask

bp = flask.Blueprint('home', __name__)


@bp.route('/')
def index():
    return flask.render_template('home.html')
