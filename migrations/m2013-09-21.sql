CREATE TABLE user2 (
	id INTEGER NOT NULL,
	email VARCHAR(120) NOT NULL,
	firstname VARCHAR(30) NOT NULL,
	lastname VARCHAR(30) NOT NULL,
	password VARCHAR(255) NOT NULL,
	active BOOLEAN,
	confirmed_at DATETIME,
	PRIMARY KEY (id),
	CHECK (active IN (0, 1))
);
INSERT INTO user2
SELECT * FROM user;
DROP TABLE user;
ALTER TABLE user2
RENAME TO user;

CREATE TABLE code_revision (
  id INTEGER NOT NULL,
  title TEXT NOT NULL,
  diff TEXT NOT NULL,
  time DATETIME NOT NULL,
  user_id INTEGER,
  program_id INTEGER,
  PRIMARY KEY (id),
  FOREIGN KEY(user_id) REFERENCES user (id),
  FOREIGN KEY(program_id) REFERENCES program (id)
);

CREATE TABLE submission2 (
	id INTEGER NOT NULL,
	title TEXT NOT NULL,
	code TEXT NOT NULL,
	submit_time DATETIME NOT NULL,
	assignment_id INTEGER,
	user_id INTEGER,
	PRIMARY KEY (id),
	FOREIGN KEY(assignment_id) REFERENCES assignment (id),
	FOREIGN KEY(user_id) REFERENCES user (id)
);

INSERT INTO submission2
SELECT id, 'Untitled Program', code, submit_time, assignment_id, user_id FROM submission;
DROP TABLE submission;
ALTER TABLE submission2
RENAME TO submission;
