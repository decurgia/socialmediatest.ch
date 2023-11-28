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

bp = Blueprint("test", __name__, url_prefix="/test")


@bp.route("/")
def index():
    db = get_db()
    tests = db.execute(
        "SELECT test_id, name, short_description, number_of_questions, pass_quota FROM test"
    ).fetchall()
    return render_template("test/index.html", tests=tests)


@bp.route("/<int:test_id>")
def detail(test_id):
    db = get_db()
    test = db.execute(
        f"SELECT test_id, name, description, number_of_questions, pass_quota FROM test WHERE test_id = {test_id}"
    ).fetchone()
    return render_template("test/detail.html", test=test)


@bp.route("/<int:test_id>/start")
def start(test_id):
    db = get_db()
    questions = db.execute(
        f"SELECT question_id FROM question WHERE question_test = {test_id}"
    ).fetchall()
    question_list = []
    for question in questions:
        question_list.append(question["question_id"])
    random.shuffle(question_list)
    session["test_id"] = test_id
    session["correct_answers"] = 0
    session["questions_answered"] = 0
    session["questions"] = question_list
    return redirect(url_for("test.question"))


@bp.route("/question", methods=("GET", "POST"))
def question():
    questions = list(session["questions"])

    if request.method == "POST":
        correct_answers = int(session["correct_answers"])
        questions_answered = int(session["questions_answered"])
        answer = int(request.form["answer"])

        db = get_db()
        correct_answer = db.execute(
            f"SELECT answer FROM question WHERE question_id = {questions[0]} AND answer = {answer}"
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
            f"SELECT question_id, question, option1, option2, option3, option4 FROM question WHERE question_id = {questions[0]}"
        ).fetchone()
        return render_template("test/question.html", question=question)
    except IndexError:
        return redirect(url_for("test.result"))


@bp.route("/result")
def result():
    email_hash = session["email_hash"]
    test_id = int(session["test_id"])
    correct_answers = int(session["correct_answers"])
    questions_answered = int(session["questions_answered"])
    test_passed = False

    db = get_db()
    test = db.execute(
        f"SELECT test_id, name, pass_quota FROM test WHERE test_id = {test_id}"
    ).fetchone()
    session['previous_answer'] = f"{correct_answers} {questions_answered}"
    test_quota = float(correct_answers / questions_answered)
    if test_quota >= float(test["pass_quota"]):
        test_passed = True
        valid_until = date.today() + timedelta(days=365)
        db = get_db()
        db.execute(
            f"INSERT OR REPLACE INTO certificate (email_hash, certificate_test, valid_until) VALUES ('{email_hash}', {test_id}, '{valid_until}')"
        )
        db.commit()

    return render_template("test/result.html", test=test, test_quota=test_quota, test_passed=test_passed)
