from time import time
import pandas as pd
from sqlalchemy import Column, Integer, Float, Date, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship

CSV_DATA_PATH = "../../data/processed/movie_metadata_clean.csv"
DATABASE = "sqlite:///../../data/db/movie.db"

Base = declarative_base()

class Genre(Base):
    __tablename__ = 'Genre'
    id = Column(Integer, primary_key=True, nullable=False) 
    name = Column(String(32))
    movies = relationship('Movie', secondary = 'movie_genres', back_populates="genres")


class Movie(Base):
    __tablename__ = 'Movie'
    id = Column(String, primary_key=True, nullable=False) 
    title = Column(String)
    year = Column(Date)
    color = Column(String)
    language = Column(String)
    country = Column(String)
    content_rating = Column(String)
    duration = Column(Integer)
    gross = Column(Integer)
    budget = Column(Integer)
    aspect_ratio = Column(Float)
    facebook_likes = Column(Integer)
    imdb_score = Column(Integer)
    num_user_for_reviews = Column(Integer)
    plot_keywords = Column(String)
    facenumber_in_poster = Column(Integer)
    genres = relationship('Genre', secondary = 'movie_genres', back_populates="movies")
    cast = relationship('Artist', secondary = 'appearances', back_populates="movies")

class Movie_Genre(Base):
    __tablename__ = 'movie_genres'
    movie_id = Column(
        String,
        ForeignKey('Movie.id'),
        primary_key = True)
    genre_id = Column(
        Integer,
        ForeignKey('Genre.id'),
        primary_key = True)
    
class Artist(Base):
    __tablename__ = 'Artist'
    __table_args__ = {'sqlite_autoincrement': True}
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, unique=True)
    movies = relationship('Movie', secondary = 'appearances', back_populates="cast")
    
class Appearance(Base):
   __tablename__ = 'appearances'
   __table_args__ = {'sqlite_autoincrement': True}
   id =  Column(Integer, primary_key=True, nullable=False)
   role = Column(String(32))
   facebook_likes = Column(Integer)
   movie_id = Column(
      Integer, 
      ForeignKey('Movie.id'), 
       primary_key = False)
   artist_id = Column(
       Integer, 
       ForeignKey('Artist.id'), 
       primary_key = False)


class User(Base):
    __tablename__ = 'User'
    __table_args__ = {'sqlite_autoincrement': True}
    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String, unique=True)
    email = Column(String(120), index=True, unique=True)
    password_hash = Column(String(128))


class seen_movies(Base):
   __tablename__ = 'seen_movies'
   __table_args__ = {'sqlite_autoincrement': True}
   id =  Column(Integer, primary_key=True, nullable=False)
   rating = Column(Integer)
   movie_id = Column(
       Integer, 
       ForeignKey('Movie.id'), 
       primary_key = False)
   user_id = Column(
       Integer, 
       ForeignKey('User.id'), 
       primary_key = False)

class recommended_movies(Base):
   __tablename__ = 'recommended_movies'
   __table_args__ = {'sqlite_autoincrement': True}
   id =  Column(Integer, primary_key=True, nullable=False)
   date = Column(Date, nullable=False)
   score = Column(Integer, nullable=False)
   movie_id = Column(
       Integer, 
       ForeignKey('Movie.id'), 
       primary_key = False)
   user_id = Column(
       Integer, 
       ForeignKey('User.id'), 
       primary_key = False)


if __name__ == "__main__":
    t = time()

    df = pd.read_csv(CSV_DATA_PATH)

    df.set_index('id')

    df = df.dropna()
    df['title_year'] = pd.to_datetime(df['title_year'], format='%Y')

    roles = ['director', 'actor_1', 'actor_2', 'actor_3']
    genres = df.iloc[:,17:41].columns

    #Create the database
    engine = create_engine(DATABASE)
    Base.metadata.create_all(engine)
    
    #Create the session
    session = sessionmaker()
    session.configure(bind=engine)
    s = session()
    
    for i, row in df.iterrows():
        movie = Movie(**{
            'id': row.id,
            'title': row.movie_title,
            'year' : row.title_year,
            'color': row.color,
            'language': row.language,
            'country': row.country,
            'content_rating': row.content_rating,
            'duration': row.duration,
            'gross': row.gross,
            'budget': row.budget,
            'aspect_ratio': row.aspect_ratio,
            'facebook_likes': row.movie_facebook_likes,
            'imdb_score': row.imdb_score,
            'num_user_for_reviews': row.num_user_for_reviews,
            'plot_keywords': row.plot_keywords,
            'facenumber_in_poster': row.facenumber_in_poster
        })
        s.add(movie) #Add all the records

        for role in roles:
            a = eval(f'row.{role}_name')
            q = s.query(Artist).filter(Artist.name==a)
            if s.query(q.exists()).scalar():
                artist_id = q.first().id
            else:
                artist = Artist(**{
                    'name': eval(f'row.{role}_name')
                })
                s.add(artist)
                s.commit()
                artist_id = q.first().id

            
            appearance = Appearance(**{
                'role': role,
                'facebook_likes': eval(f'row.{role}_facebook_likes'),
                'artist_id': artist_id,
                'movie_id': movie.id
            })
            s.add(appearance)
        
    for genre in genres:
        grp = df.groupby(genre)
 
        g = Genre(**{
            'name': genre
        })
        s.add(g)

        for i in grp.get_group(1).id.to_list():
            m = s.query(Movie).get(i)
            a = Movie_Genre(**{
                'movie_id': m.id,
                'genre_id': g.id
            })
            s.add(a)
        
    u = User(**{
        'username': 'charlie',
        'email': 'charlie.chaplin@moviette.com',
        'password_hash': ''
    })
    s.add(u)
    
    s.commit() #Attempt to commit all the records
    s.close()

    print("Time elapsed: " + str(time() - t) + " s.")
