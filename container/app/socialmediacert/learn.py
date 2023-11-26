from flask import render_template, Blueprint


bp = Blueprint("learn", __name__, url_prefix="/learn")


@bp.route("/")
def index():
    return render_template("learn/index.html")
