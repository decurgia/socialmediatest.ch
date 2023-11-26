from flask import render_template
from flask import Blueprint

from .db import get_db

bp = Blueprint("test", __name__, url_prefix="/test")


@bp.route("/")
def index():
    db = get_db()
    questions = db.execute(
        f"SELECT id, question, option1, option2, option3, option4 FROM question"
    ).fetchall()
    return render_template("test/index.html", questions=questions)
