DELETE FROM practice_problem_template;
DELETE FROM practice_problem_concept;
DELETE FROM submissions_concepts;
DELETE FROM templates_concepts;

CREATE TABLE practice_problem_submission2 (
  id INTEGER NOT NULL,
  code TEXT NOT NULL,
  result_test TEXT NOT NULL,
  result_test_error BOOLEAN NOT NULL,
  result_no_test TEXT NOT NULL,
  result_no_test_error BOOLEAN NOT NULL,
  got_hint BOOLEAN NOT NULL,
  gave_up BOOLEAN NOT NULL,
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
  CHECK (gave_up IN (0, 1)),
  CHECK (correct IN (0, 1)),
  FOREIGN KEY(problem_id) REFERENCES practice_problem_template (id),
  FOREIGN KEY(user_id) REFERENCES user (id)
);
DROP TABLE practice_problem_submission;
ALTER TABLE practice_problem_submission2
RENAME TO practice_problem_submission;
