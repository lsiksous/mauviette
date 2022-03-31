from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/movie.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

Base = automap_base()
Base.prepare(db.engine, reflect=True)

Movie = Base.classes.Movie
Artist = Base.classes.Artist
Genre = Base.classes.Genre


@app.route('/')
def index():
    genres = db.session.query(Genre).all()

    for g in genres:
        print(g.name)
    return ''

if __name__ == "__main__":
    app.run()
