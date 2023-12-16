from flask import render_template
from flask import Blueprint
from flask import session
from flask import redirect
from flask import url_for
from flask import request
from datetime import date
from datetime import timedelta
import random

from .db import get_db
from . import get_locale

bp = Blueprint("test", __name__, url_prefix="/test")


@bp.route("/")
def index():
    db = get_db()
    tests = db.execute(
        "SELECT id, name, short_description, number_of_questions, pass_quota FROM test WHERE locale = ?",
        (get_locale(),),
    ).fetchall()
    return render_template("test/index.html", tests=tests)


@bp.route("/<int:test_id>")
def detail(test_id):
    db = get_db()
    test = db.execute(
        "SELECT id, name, description, number_of_questions, pass_quota FROM test WHERE id = ? AND locale = ?",
        (
            test_id,
            get_locale(),
        ),
    ).fetchone()
    return render_template("test/detail.html", test=test)


@bp.route("/<int:test_id>/start", methods=("GET", "POST"))
def start(test_id):
    if request.method == "POST":
        # get email from the form
        email = request.form["email"]
        if not email:
            session.clear()
            return redirect(url_for("test.start", test_id=test_id))

        # get Test detail
        db = get_db()
        test = db.execute(
            "SELECT number_of_questions FROM test WHERE id = ? AND locale = ?",
            (
                test_id,
                get_locale(),
            ),
        ).fetchone()

        # get the related questions and shuffle
        questions = db.execute(
            "SELECT id FROM question WHERE fk_test_id = ? AND locale = ?",
            (
                test_id,
                get_locale(),
            ),
        ).fetchall()
        question_list = []
        for question in questions:
            question_list.append(question["id"])
        random.shuffle(question_list)

        # put everything into the session
        session["email"] = email.strip()
        session["test_id"] = test_id
        session["correct_answers"] = 0
        session["questions_answered"] = 0
        session["questions"] = question_list[: test["number_of_questions"]]
        return redirect(url_for("test.question"))

    db = get_db()
    test = db.execute(
        "SELECT id, name, description, number_of_questions, pass_quota FROM test WHERE id = ? AND locale = ?",
        (
            test_id,
            get_locale(),
        ),
    ).fetchone()
    return render_template("test/start.html", test=test)


@bp.route("/question", methods=("GET", "POST"))
def question():
    locale = get_locale()
    questions = list(session["questions"])

    if request.method == "POST":
        correct_answers = int(session["correct_answers"])
        questions_answered = int(session["questions_answered"])
        answer = int(request.form["answer"])

        db = get_db()
        correct_answer = db.execute(
            "SELECT answer FROM question WHERE id = ? AND locale = ? AND answer = ?",
            (
                questions[0],
                locale,
                answer,
            ),
        ).fetchone()
        # if record queried, then the answer is correct
        if correct_answer:
            session["correct_answers"] = correct_answers + 1
        # go to next question
        session["questions_answered"] = questions_answered + 1

        del questions[0]
        session["questions"] = questions
        return redirect(url_for("test.question"))

    try:
        db = get_db()
        question = db.execute(
            "SELECT id, question, option1, option2, option3, option4 FROM question WHERE id = ? AND locale = ?",
            (
                questions[0],
                locale,
            ),
        ).fetchone()
        return render_template("test/question.html", question=question)
    except IndexError:
        return redirect(url_for("test.result"))


@bp.route("/result")
def result():
    test_id = int(session["test_id"])
    correct_answers = int(session["correct_answers"])
    questions_answered = int(session["questions_answered"])
    test_passed = False

    db = get_db()
    test = db.execute(
        "SELECT id, name, pass_quota FROM test WHERE id = ? AND locale = ?",
        (
            test_id,
            get_locale(),
        ),
    ).fetchone()
    test_quota = float(correct_answers / questions_answered)
    if "email" in session and test_quota >= float(test["pass_quota"]):
        import hashlib

        email = session["email"]
        email_hash = hashlib.sha256(email.encode("utf-8").strip().lower()).hexdigest()
        test_passed = True
        valid_until = date.today() + timedelta(days=365)
        certificate = (
            {
                "email_hash": email_hash,
                "certificate_test": test_id,
                "valid_until": valid_until,
            },
        )
        db = get_db()
        db.executemany(
            "INSERT OR REPLACE INTO certificate VALUES(:email_hash, :certificate_test, :valid_until)",
            certificate,
        )
        db.commit()

    return render_template(
        "test/result.html", test=test, test_quota=test_quota, test_passed=test_passed
    )
