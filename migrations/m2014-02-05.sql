CREATE TABLE quiz2 (
  id INTEGER NOT NULL,
  name VARCHAR(30) NOT NULL,
  week INTEGER NOT NULL,
  deadline DATETIME NOT NULL,
  PRIMARY KEY (id)
);

DROP TABLE quiz;
ALTER TABLE quiz2
RENAME TO quiz;

CREATE TABLE quiz_response2 (
  id INTEGER NOT NULL,
  submit_time DATETIME NOT NULL,
  quiz_id INTEGER NOT NULL,
  question_id INTEGER NOT NULL,
  user_id INTEGER NOT NULL,
  user_answer VARCHAR(100) NOT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY(quiz_id) REFERENCES quiz (id),
  FOREIGN KEY(question_id) REFERENCES quiz_question (id),
  FOREIGN KEY(user_id) REFERENCES user (id)
);

DROP TABLE quiz_response;
ALTER TABLE quiz_response2
RENAME TO quiz_response;
