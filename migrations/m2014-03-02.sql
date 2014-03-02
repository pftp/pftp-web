-- Add website column to user table

CREATE TABLE user2 (
  id INTEGER NOT NULL,
  email VARCHAR(120) NOT NULL,
  firstname VARCHAR(30) NOT NULL,
  lastname VARCHAR(30) NOT NULL,
  password VARCHAR(255) NOT NULL,
  active BOOLEAN,
  website VARCHAR(120),
  confirmed_at DATETIME,
  PRIMARY KEY (id),
  CHECK (active IN (0, 1))
);

INSERT INTO user2
SELECT id, email, firstname, lastname, password, active, '', confirmed_at FROM user;
DROP TABLE user;
ALTER TABLE user2
RENAME TO user;
