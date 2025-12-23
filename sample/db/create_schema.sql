USE spotify;

CREATE TABLE artists (
	id VARCHAR(64) PRIMARY KEY,
	name VARCHAR(255) NOT NULL,
    genres TEXT,
    popularity INT,
    followers INT,
    image_url TEXT,
    type VARCHAR(64) NOT NULL DEFAULT 'artist'
    );

CREATE TABLE tracks (
	id VARCHAR(64) PRIMARY KEY,
	name VARCHAR(255) NOT NULL,
    release_date VARCHAR(7),
    popularity INT,
    artist_id VARCHAR(64) NOT NULL,
    artist_name VARCHAR(255),
    album_id VARCHAR(64) NOT NULL,
    album_name VARCHAR(255),
    album_image_url TEXT,
    type VARCHAR(64) NOT NULL DEFAULT 'track',
	FOREIGN KEY (artist_id) REFERENCES artists(id)
	);
    