import os

from flask import Flask, render_template


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'db.sqlite'),
        UPLOADS_DIR=os.path.join(app.instance_path, 'uploads'),
        MAX_CONTENT_LENGTH=2**24, # 16 MB
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # ensure the uploads folder exists
    try:
        os.makedirs(app.config['UPLOADS_DIR'])
    except OSError:
        pass

    from . import db
    db.init_app(app)

    from . import cli
    cli.init_app(app)

    from . import index
    app.register_blueprint(index.bp)

    from . import service
    app.register_blueprint(service.bp)

    app.add_url_rule('/', endpoint='index')

    return app
