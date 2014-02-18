CREATE TABLE assignment2 (
  id INTEGER NOT NULL,
  name VARCHAR(100) NOT NULL,
  semester VARCHAR(100) NOT NULL,
  href TEXT NOT NULL,
  description TEXT NOT NULL,
  deadline DATETIME NOT NULL,
  points INTEGER NOT NULL,
  PRIMARY KEY (id)
);

INSERT INTO assignment2
SELECT id, name, 'fa13', '/', description, deadline, points FROM assignment;

DROP TABLE assignment;
ALTER TABLE assignment2
RENAME TO assignment;

CREATE TABLE grade2 (
  id INTEGER NOT NULL,
  score INTEGER NOT NULL,
  submitted DATETIME NOT NULL,
  user_id INTEGER,
  assignment_id INTEGER,
  PRIMARY KEY (id),
  FOREIGN KEY(user_id) REFERENCES user (id),
  FOREIGN KEY(assignment_id) REFERENCES assignment (id)
);

INSERT INTO grade2
SELECT id, score, '2013-12-25 00:00:00.000000', user_id, assignment_id from grade;

DROP TABLE grade;
ALTER TABLE grade2
RENAME TO grade;

CREATE TABLE quiz2 (
  id INTEGER NOT NULL,
  name VARCHAR(30) NOT NULL,
  week INTEGER NOT NULL,
  deadline DATETIME NOT NULL,
  assignment_id INTEGER,
  PRIMARY KEY (id),
  FOREIGN KEY(assignment_id) REFERENCES assignment (id)
);

INSERT INTO quiz2
SELECT id, name, week, deadline, null from quiz;

DROP TABLE quiz;
ALTER TABLE quiz2
RENAME TO quiz;
