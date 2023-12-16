import os

from flask import Flask
from flask import render_template
from flask import request
from flask import send_from_directory

from flask_babel import Babel


def get_locale():
    return request.accept_languages.best_match(["en", "de"])


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    babel = Babel(app, locale_selector=get_locale)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "socialmediatest.sqlite"),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db

    db.init_app(app)

    @app.route("/")
    def index():
        if get_locale() == "de":
            return render_template("index_de.html")
        return render_template("index_en.html")

    @app.route("/about")
    def about():
        if get_locale() == "de":
            return render_template("about_de.html")
        return render_template("about.html")

    @app.route("/favicon.ico")
    @app.route("/robots.txt")
    def static_from_root():
        return send_from_directory(app.static_folder, request.path[1:])

    from . import learn
    from . import test
    from . import certificate

    app.register_blueprint(learn.bp)
    app.register_blueprint(test.bp)
    app.register_blueprint(certificate.bp)

    return app
