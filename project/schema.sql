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
