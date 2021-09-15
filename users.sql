-- from the terminal run:
-- psql < users.sql

DROP DATABASE IF EXISTS blogly;

CREATE DATABASE blogly;

\c blogly

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    profile_pic TEXT DEFAULT 'https://images.freeimages.com/images/large-previews/b3d/flowers-1375316.jpg'
);