CREATE TABLE code_run (
  id INTEGER NOT NULL,
  title TEXT NOT NULL,
  code TEXT NOT NULL,
  output TEXT,
  error TEXT,
  time DATETIME NOT NULL,
  user_id INTEGER,
  program_id INTEGER,
  PRIMARY KEY (id),
  FOREIGN KEY(user_id) REFERENCES user (id),
  FOREIGN KEY(program_id) REFERENCES program (id)
);
