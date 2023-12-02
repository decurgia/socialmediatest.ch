from flask import request
from flask import render_template
from flask import Blueprint
from flask import session

import hashlib
from datetime import date
from datetime import timedelta

from .db import get_db
from . import get_locale

bp = Blueprint("certificate", __name__, url_prefix="/certificate")


@bp.route("/")
def index():
    certificates = []
    if "email_hash" in session:
        email_hash = session["email_hash"]
        db = get_db()
        certificates = db.execute(
            "SELECT test.id, test.name, certificate.valid_until FROM certificate INNER JOIN test ON certificate.fk_test_id = test.id AND test.locale = ? WHERE email_hash = ?",
            (
                get_locale(),
                email_hash,
            ),
        ).fetchall()
    return render_template("certificate/index.html", certificates=certificates)
