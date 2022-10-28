-- Add database data that should be pre-initialized here
--
-- Note that we only run this when the actual app runs
-- so stuff in here will not show up in tests

-- tags need conditional insert to prevent UNIQUE constraint issues
INSERT INTO tags VALUES
  (1, 'vegan'),
  (2, 'mexican'),
  (3, 'italian')
ON CONFLICT (id) DO UPDATE
SET name = EXCLUDED.name;

