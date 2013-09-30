CREATE TABLE lab_program (
  id INTEGER NOT NULL,
  section INTEGER NOT NULL,
  lab_id INTEGER NOT NULL,
  user_id INTEGER,
  program_id INTEGER,
  PRIMARY KEY (id),
  FOREIGN KEY(user_id) REFERENCES user (id),
  FOREIGN KEY(program_id) REFERENCES program (id)
);
