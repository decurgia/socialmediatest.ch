from flask import request
from flask import render_template
from flask import Blueprint
from flask import flash
from flask import redirect
from flask import url_for
from flask import session

import hashlib
from datetime import date
from datetime import timedelta

from .db import get_db

bp = Blueprint("certificate", __name__, url_prefix="/certificate")


@bp.route("/")
def index():
    certificates = []
    if "email_hash" in session:
        db = get_db()
        certificates = db.execute(
            f"SELECT test.name, certificate.valid_until FROM certificate INNER JOIN test ON certificate.certificate_test = test.test_id WHERE email_hash = '{session['email_hash']}'"
        ).fetchall()
    return render_template("certificate/index.html", certificates=certificates)
