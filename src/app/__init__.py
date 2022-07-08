from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from src.config import Config


app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

login = LoginManager(app)
login.login_view = 'login'

bootstrap = Bootstrap(app)

Base = automap_base()
Base.prepare(db.engine, reflect=True)

Movie = Base.classes.Movie
Artist = Base.classes.Artist
Genre = Base.classes.Genre

session = sessionmaker()
session.configure(bind=db.engine)
s = session()

from src.app import routes, models
