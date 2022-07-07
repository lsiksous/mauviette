from flask import Flask, render_template, flash, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
from flask_bootstrap import Bootstrap
from flask_login import login_user, logout_user, current_user, login_required, LoginManager
#from flask_cors import CORS
from forms import LoginForm
import models


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../../data/movie.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

login = LoginManager()
login.login_view = "login"

bootstrap = Bootstrap(app)

db = SQLAlchemy(app)

Base = automap_base()
Base.prepare(db.engine, reflect=True)

Movie = Base.classes.Movie
Artist = Base.classes.Artist
Genre = Base.classes.Genre

@app.route("/", methods=["GET", "POST"])
#@login_required
def index():
    return render_template('index.html')


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

if __name__ == "__main__":
    app.run()
