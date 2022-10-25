-- A SQL script that creates the necessary tables IF they do not exist in the
-- database. This script is executed every time when the app starts.
--
-- Do not add default values (in given clauses of testing) in here

CREATE TABLE IF NOT EXISTS accounts (
  -- both name and email must be UNIQUE

  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL UNIQUE,
  email TEXT NOT NULL UNIQUE,
  password TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS recipes (
  id SERIAL PRIMARY KEY,
  title TEXT NOT NULL,
  prep_time TIME,
  cook_time TIME,
  directions TEXT NOT NULL, -- assume it's all lumped as markdown text or sth
  author INTEGER NOT NULL REFERENCES accounts (id)
    ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS ingredients (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  quantity TEXT NOT NULL,
  recipe INTEGER NOT NULL REFERENCES recipes (id)
    ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS comments (
  id SERIAL PRIMARY KEY,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  author INTEGER REFERENCES accounts (id)
    ON DELETE SET NULL,
  recipe INTEGER NOT NULL REFERENCES recipes (id)
    ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS tags (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS recipe_tags (
  recipe INTEGER NOT NULL REFERENCES recipes (id)
    ON DELETE CASCADE,
  tag INTEGER NOT NULL REFERENCES tags (id)
    ON DELETE CASCADE,

  PRIMARY KEY (recipe, tag)
);
