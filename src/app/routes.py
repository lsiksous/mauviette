from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import MessageForm, LoginForm
from app.models import User, Message


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    max_usage = 1000
    language = ""
    inspire = ""
    correct = ""
    suggest = ""
    mistakes = []
    replacements = []
    message = {"body": "", "language": ""}

    form = MessageForm()

    if request.method == "POST":
        message = Message(body=request.form["message"], language="fr")
        correct, mistakes, replacements = message.correct()
        if current_user.quota <= max_usage:
            # flash(
            #    "You have " + str(max_usage - current_user.quota) + " suggestions left."
            # )
            inspire, suggest = message.suggest(request.form["dialect"])
            current_user.quota += 1
            message.suggestions = suggest
            message.user_id = current_user.id
            db.session.add(message)
            db.session.commit()
        else:
            flash("You have reached your suggestions quota.")
            suggest = ""
            message = {"body": message.body, "language": message.language}
    else:
        message = {"body": "Bonjour", "language": "fr"}
        correct = "Bonjour"

    return render_template(
        "index.html",
        form=form,
        message=message,
        language=language,
        inspire=inspire,
        suggest=suggest,
        correct=correct,
        mistakes=mistakes,
        replacements=replacements,
        len_miss=len(mistakes),
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("login"))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("index")
        return redirect(next_page)
    return render_template("login.html", title="Sign In", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))
