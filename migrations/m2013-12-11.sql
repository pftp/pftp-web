CREATE TABLE practice_problem_concept2 (
  id INTEGER NOT NULL,
  name TEXT NOT NULL,
  display_name TEXT,
  explanation TEXT,
  PRIMARY KEY (id)
);

INSERT INTO practice_problem_concept2
SELECT id, name, name, '' FROM practice_problem_concept;

DROP TABLE practice_problem_concept;
ALTER TABLE practice_problem_concept2
RENAME TO practice_problem_concept;

