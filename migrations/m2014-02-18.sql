CREATE TABLE homework (
  id INTEGER NOT NULL,
  week INTEGER NOT NULL,
  deadline DATETIME NOT NULL,
  assignment_id INTEGER,
  PRIMARY KEY (id),
  FOREIGN KEY(assignment_id) REFERENCES assignment (id)
);
CREATE TABLE homework_problem (
  id INTEGER NOT NULL,
  deadline DATETIME NOT NULL,
  homework_id INTEGER,
  template_id INTEGER,
  PRIMARY KEY (id),
  FOREIGN KEY(homework_id) REFERENCES homework (id),
  FOREIGN KEY(template_id) REFERENCES practice_problem_template (id)
);
