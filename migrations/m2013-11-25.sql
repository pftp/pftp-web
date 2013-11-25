DROP TABLE practice_problem_submissions;
DROP TABLE practice_problem_template;

CREATE TABLE practice_problem_concept (
  id INTEGER NOT NULL,
  name TEXT NOT NULL,
  PRIMARY KEY (id)
);
CREATE TABLE practice_problem_submission (
  id INTEGER NOT NULL,
  code TEXT NOT NULL,
  result_test TEXT NOT NULL,
  result_test_error BOOLEAN NOT NULL,
  result_no_test TEXT NOT NULL,
  result_no_test_error BOOLEAN NOT NULL,
  got_hint BOOLEAN NOT NULL,
  correct BOOLEAN NOT NULL,
  started DATETIME NOT NULL,
  submitted DATETIME NOT NULL,
  template_vars TEXT NOT NULL,
  problem_id INTEGER NOT NULL,
  user_id INTEGER NOT NULL,
  PRIMARY KEY (id),
  CHECK (result_test_error IN (0, 1)),
  CHECK (result_no_test_error IN (0, 1)),
  CHECK (got_hint IN (0, 1)),
  CHECK (correct IN (0, 1)),
  FOREIGN KEY(problem_id) REFERENCES practice_problem_template (id),
  FOREIGN KEY(user_id) REFERENCES user (id)
);
CREATE TABLE practice_problem_template (
  id INTEGER NOT NULL,
  problem_name TEXT NOT NULL,
  prompt TEXT NOT NULL,
  solution TEXT NOT NULL,
  test TEXT NOT NULL,
  hint TEXT NOT NULL,
  gen_template_vars TEXT NOT NULL,
  is_current BOOLEAN NOT NULL,
  PRIMARY KEY (id),
  CHECK (is_current IN (0, 1))
);
CREATE TABLE submissions_concepts (
  practice_problem_submission_id INTEGER,
  practice_problem_concept_id INTEGER,
  FOREIGN KEY(practice_problem_submission_id) REFERENCES practice_problem_submission (id),
  FOREIGN KEY(practice_problem_concept_id) REFERENCES practice_problem_concept (id)
);
CREATE TABLE templates_concepts (
  practice_problem_template_id INTEGER,
  practice_problem_concept_id INTEGER,
  FOREIGN KEY(practice_problem_template_id) REFERENCES practice_problem_template (id),
  FOREIGN KEY(practice_problem_concept_id) REFERENCES practice_problem_concept (id)
);
