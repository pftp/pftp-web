CREATE TABLE practice_problem_submissions_2 (
  id INTEGER NOT NULL,
  problem_id INTEGER,
  user_id INTEGER NOT NULL,
  code VARCHAR(500) NOT NULL,
  result_test VARCHAR(500) NOT NULL,
  result_no_test VARCHAR(500) NOT NULL,
  got_hint BOOLEAN NOT NULL,
  correct BOOLEAN NOT NULL,
  started DATETIME NOT NULL,
  submitted DATETIME NOT NULL,
  template_vars VARCHAR(500),
  PRIMARY KEY (id),
  FOREIGN KEY(problem_id) REFERENCES practice_problem_template (id),
  FOREIGN KEY(user_id) REFERENCES user (id),
  CHECK (got_hint IN (0, 1)),
  CHECK (correct IN (0, 1))
);



INSERT INTO practice_problem_submissions_2
SELECT * FROM practice_problem_submissions;
DROP TABLE practice_problem_submissions;
ALTER TABLE practice_problem_submissions_2
RENAME TO practice_problem_submissions;
