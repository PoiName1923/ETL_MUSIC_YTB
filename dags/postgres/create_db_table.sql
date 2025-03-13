
--- Create database if not exists
DO $$ 
BEGIN 
    IF NOT EXISTS (SELECT FROM pg_database WHERE datname = 'MUSIC_DATABASE') THEN
        CREATE DATABASE MUSIC_DATABASE;
    END IF;
END $$;

--- Create table if not exists
CREATE TABLE IF NOT EXISTS ARTISTS (
    channel_id VARCHAR(20) PRIMARY KEY,
    artist_name VARCHAR(255) NOT NULL,
    execution_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

--- Create table if not exists
CREATE TABLE IF NOT EXISTS ARTIST_SONGS (
    video_id VARCHAR(20) PRIMARY KEY,
    channel_id VARCHAR(20),
    title VARCHAR(255) NOT NULL,
    author VARCHAR(100),
    duration INT,
    views INT,
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    thumbnail VARCHAR(200),
    url VARCHAR(255),
    execution_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (channel_id) REFERENCES ARTISTS(channel_id)
);
