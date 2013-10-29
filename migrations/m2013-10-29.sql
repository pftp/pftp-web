CREATE TABLE practice_problem_submissions (
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
  PRIMARY KEY (id),
  FOREIGN KEY(problem_id) REFERENCES practice_problem_template (id),
  FOREIGN KEY(user_id) REFERENCES user (id),
  CHECK (got_hint IN (0, 1)),
  CHECK (correct IN (0, 1))
);


CREATE TABLE practice_problem_template (
  id INTEGER NOT NULL,
  problem_dir VARCHAR(20) NOT NULL,
  prompt VARCHAR(500) NOT NULL,
  solution VARCHAR(500) NOT NULL,
  test VARCHAR(500) NOT NULL,
  hint VARCHAR(500) NOT NULL,
  template_vars VARCHAR(500) NOT NULL,
  is_current BOOLEAN NOT NULL,
  PRIMARY KEY (id),
  CHECK (is_current IN (0, 1))
);
