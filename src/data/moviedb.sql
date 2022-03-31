CREATE TABLE "Artist" (
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
	name VARCHAR, 
	UNIQUE (name)
)
;

CREATE TABLE "Genre" (
	id INTEGER NOT NULL, 
	name VARCHAR(32), 
	PRIMARY KEY (id)
)
;

CREATE TABLE "Movie" (
	id VARCHAR NOT NULL, 
	title VARCHAR, 
	year DATE, 
	color VARCHAR, 
	language VARCHAR, 
	country VARCHAR, 
	content_rating VARCHAR, 
	duration INTEGER, 
	gross INTEGER, 
	budget INTEGER, 
	aspect_ratio FLOAT, 
	facebook_likes INTEGER, 
	imdb_score INTEGER, 
	num_user_for_reviews INTEGER, 
	plot_keywords VARCHAR, 
	facenumber_in_poster INTEGER, 
	PRIMARY KEY (id)
)
;

CREATE TABLE appearances (
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
	role VARCHAR(32), 
	facebook_likes INTEGER, 
	movie_id INTEGER, 
	artist_id INTEGER, 
	FOREIGN KEY(movie_id) REFERENCES "Movie" (id), 
	FOREIGN KEY(artist_id) REFERENCES "Artist" (id)
)
;

CREATE TABLE movie_genres (
	movie_id VARCHAR NOT NULL, 
	genre_id INTEGER NOT NULL, 
	PRIMARY KEY (movie_id, genre_id), 
	FOREIGN KEY(movie_id) REFERENCES "Movie" (id), 
	FOREIGN KEY(genre_id) REFERENCES "Genre" (id)
)
;

