CREATE TABLE IF NOT EXISTS accounts (
  -- both name and email must be UNIQUE

  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL UNIQUE,
  email TEXT NOT NULL UNIQUE,
  password TEXT NOT NULL
);
