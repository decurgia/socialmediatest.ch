import os

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import session
from flask import flash

from flask_babel import Babel

import hashlib


def get_locale():
    return request.accept_languages.best_match(["en", "de"])


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    babel = Babel(app, locale_selector=get_locale)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "socialmediacert.sqlite"),
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
        return render_template("index.html")

    @app.route("/about")
    def about():
        return render_template("about.html")

    @app.route("/email", methods=("GET", "POST"))
    def email():
        if request.method == "POST":
            email = request.form["email"]

            if not email:
                session["email"] = ""
                session["email_hash"] = ""
            else:
                session["email"] = email.strip()
                session["email_hash"] = hashlib.sha256(
                    email.encode("utf-8").strip().lower()
                ).hexdigest()
            return redirect(url_for("email"))
        return render_template("email.html")

    from . import learn
    from . import test
    from . import certificate

    app.register_blueprint(learn.bp)
    app.register_blueprint(test.bp)
    app.register_blueprint(certificate.bp)

    return app
