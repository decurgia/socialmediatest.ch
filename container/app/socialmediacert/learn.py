from flask import render_template, Blueprint
from . import get_locale

bp = Blueprint("learn", __name__, url_prefix="/learn")


@bp.route("/")
def index():
    if get_locale() is "de":
        return render_template("learn/index_de.html")
    return render_template("learn/index.html")
