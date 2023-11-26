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
            f"SELECT email_hash, valid_until FROM certificate WHERE email_hash = '{session['email_hash']}'"
        ).fetchall()
    return render_template("certificate/index.html", certificates=certificates)


@bp.route("/create", methods=("GET", "POST"))
def create():
    if request.method == "POST":
        email = request.form["email"]
        error = None

        if not email:
            error = "Email is required."

        if error is not None:
            flash(error)
        else:
            email_hash = hashlib.sha256(email.encode("utf-8").lower()).hexdigest()
            valid_until = date.today() + timedelta(days=365)
            db = get_db()
            db.execute(
                "INSERT OR REPLACE INTO certificate (email_hash, valid_until) VALUES (?, ?)",
                (email_hash, valid_until),
            )
            db.commit()
            return redirect(url_for("certificate.index"))

    return render_template("certificate/create.html")
