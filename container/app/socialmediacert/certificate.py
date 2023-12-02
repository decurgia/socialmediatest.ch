from flask import request
from flask import render_template
from flask import Blueprint
from flask import session

import hashlib
from datetime import date
from datetime import timedelta

from .db import get_db

bp = Blueprint("certificate", __name__, url_prefix="/certificate")


@bp.route("/")
def index():
    certificates = []
    if "email" in session:
        email = session["email"]
        email_hash = hashlib.sha256(email.encode("utf-8").strip().lower()).hexdigest()
        db = get_db()
        certificates = db.execute(
            "SELECT test.id, test.name, certificate.valid_until FROM certificate INNER JOIN test ON certificate.fk_test_id = test.id AND test.locale = ? WHERE email_hash = ?",
            (
                request.accept_languages.best_match(["en", "de"]),
                email_hash,
            ),
        ).fetchall()
    return render_template("certificate/index.html", certificates=certificates)
