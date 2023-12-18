from flask import request
from flask import render_template
from flask import Blueprint
from flask import session
from flask import redirect
from flask import url_for

from datetime import date
from datetime import timedelta

from .db import get_db
from . import get_locale

bp = Blueprint("certificate", __name__, url_prefix="/certificate")


@bp.route("", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        email = request.form["email"]

        if not email:
            session.clear()
        else:
            session["email"] = email.strip()
        return redirect(url_for("certificate.index"))

    certificates = []
    if "email" in session:
        import hashlib

        email = session["email"]
        email_hash = hashlib.sha256(email.encode("utf-8").strip().lower()).hexdigest()
        db = get_db()
        certificates = db.execute(
            "SELECT test.id, test.name, certificate.valid_until FROM certificate INNER JOIN test ON certificate.fk_test_id = test.id AND test.locale = ? WHERE email_hash = ?",
            (
                get_locale(),
                email_hash,
            ),
        ).fetchall()
    return render_template("certificate/index.html", certificates=certificates)


@bp.route("/<int:test_id>")
def detail(test_id):
    if "email" in session:
        import hashlib

        email = session["email"]
        email_hash = hashlib.sha256(email.encode("utf-8").strip().lower()).hexdigest()
        db = get_db()
        certificate = db.execute(
            "SELECT test.name, test.description, test.number_of_questions, test.pass_quota, certificate.valid_until FROM certificate INNER JOIN test ON certificate.fk_test_id = test.id AND test.locale = ? WHERE email_hash = ? AND fk_test_id = ?",
            (
                get_locale(),
                email_hash,
                test_id,
            ),
        ).fetchone()
    return render_template("certificate/detail.html", certificate=certificate)
