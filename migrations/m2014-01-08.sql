-- Migration to add language table and FK to app practice problems

CREATE TABLE "language" (
  id INTEGER NOT NULL,
  language TEXT NOT NULL,
  PRIMARY KEY (id)
);
INSERT INTO "language" (id, language) VALUES
(1, "python"),
(2, "javascript");

--
-- Add language to practice_problem_template table
--
CREATE TABLE "practice_problem_template2" (
  id INTEGER NOT NULL,
  problem_name TEXT NOT NULL,
  prompt TEXT NOT NULL,
  solution TEXT NOT NULL,
  test TEXT NOT NULL,
  hint TEXT NOT NULL,
  gen_template_vars TEXT NOT NULL,
  is_current BOOLEAN NOT NULL,
  language_id INTEGER NOT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (language_id) REFERENCES language (id),
  CHECK (is_current IN (0, 1))
);

INSERT INTO "practice_problem_template2"
-- Existing problems are all in Python
-- Assume Python is language 1
SELECT id, problem_name, prompt, solution, test, hint, gen_template_vars, is_current, 1 FROM practice_problem_template;

DROP TABLE practice_problem_template;
ALTER TABLE "practice_problem_template2"
RENAME TO practice_problem_template;


--
-- Add language to practice_problem_submission table
--
CREATE TABLE "practice_problem_submission2" (
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
  language_id INTEGER NOT NULL,
  PRIMARY KEY (id),
  CHECK (result_test_error IN (0, 1)),
  CHECK (result_no_test_error IN (0, 1)),
  CHECK (got_hint IN (0, 1)),
  CHECK (gave_up IN (0, 1)),
  CHECK (correct IN (0, 1)),
  FOREIGN KEY(problem_id) REFERENCES practice_problem_template (id),
  FOREIGN KEY(user_id) REFERENCES user (id),
  FOREIGN KEY (language_id) REFERENCES language (id)
);

INSERT INTO practice_problem_submission2
-- Existing problems are all in Python
-- Assume Python is language 1
SELECT id, code, result_test, result_test_error, result_no_test, result_no_test_error, got_hint, gave_up, correct, started, submitted, template_vars, problem_id, user_id, 1 FROM practice_problem_submission;

DROP TABLE practice_problem_submission;
ALTER TABLE practice_problem_submission2
RENAME TO practice_problem_submission;


--
-- Add language to practice_problem_concept table
--
CREATE TABLE "practice_problem_concept2" (
  id INTEGER NOT NULL,
  name TEXT NOT NULL,
  display_name TEXT,
  explanation TEXT,
  language_id INTEGER NOT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (language_id) REFERENCES language (id)
);

INSERT INTO practice_problem_concept2
-- Existing problems are all in Python
-- Assume Python is language 1
SELECT id, name, display_name, explanation, 1 FROM practice_problem_concept;

DROP TABLE practice_problem_concept;
ALTER TABLE practice_problem_concept2
RENAME TO practice_problem_concept;
