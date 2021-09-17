-- from the terminal run:
-- psql < blogly.sql

DROP DATABASE IF EXISTS blogly;

CREATE DATABASE blogly;

\c blogly

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    first_name TEXT NOT NULL UNIQUE,
    last_name TEXT NOT NULL UNIQUE,
    profile_pic TEXT DEFAULT 'https://images.freeimages.com/images/large-previews/b3d/flowers-1375316.jpg'
);

CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    title VARCHAR(25) NOT NULL,
    content TEXT NOT NULL,
    created_at TEXT NOT NULL,
    posted_by INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE
);