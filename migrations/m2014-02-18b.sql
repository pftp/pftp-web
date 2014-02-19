CREATE TABLE practice_problem_template2 (
  id INTEGER NOT NULL,
  problem_name TEXT NOT NULL,
  prompt TEXT NOT NULL,
  solution TEXT NOT NULL,
  test TEXT NOT NULL,
  hint TEXT NOT NULL,
  gen_template_vars TEXT NOT NULL,
  is_current BOOLEAN NOT NULL,
  is_homework BOOLEAN NOT NULL,
  language_id INTEGER NOT NULL,
  PRIMARY KEY (id),
  CHECK (is_current IN (0, 1)),
  CHECK (is_homework IN (0, 1)),
  FOREIGN KEY(language_id) REFERENCES language (id)
);

INSERT INTO practice_problem_template2
SELECT id, problem_name, prompt, solution, test, hint, gen_template_vars, is_current, 0, language_id from practice_problem_template;

DROP TABLE practice_problem_template;
ALTER TABLE practice_problem_template2
RENAME TO practice_problem_template;
