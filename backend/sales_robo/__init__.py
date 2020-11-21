import os

from flask import Flask
from flask_cors import CORS

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        UPLOAD_FOLDER=os.path.join(
            os.path.dirname(__file__),
            '_upload'
        )
    )
    CORS(app)

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

    # a simple page that says hello
    @app.route('/health')
    def healthcheck():
        return 'Hello, World!'

    from . import products, misc_data, search, sales_data

    app.register_blueprint(products.bp)
    app.register_blueprint(misc_data.bp)
    app.register_blueprint(search.bp)
    app.register_blueprint(sales_data.bp)

    return app
