CREATE TABLE quiz (
  id INTEGER NOT NULL,
  name VARCHAR(30) NOT NULL,
  week INTEGER NOT NULL,
  PRIMARY KEY (id)
);


CREATE TABLE quiz_question (
  id INTEGER NOT NULL,
  question VARCHAR(1000) NOT NULL,
  answer_choices VARCHAR(7000) NOT NULL,
  solution VARCHAR(100) NOT NULL,
  quiz_id INTEGER,
  PRIMARY KEY (id),
  FOREIGN KEY(quiz_id) REFERENCES quiz (id)
);


CREATE TABLE quiz_response (
  id INTEGER NOT NULL,
  question_id INTEGER NOT NULL,
  user_id INTEGER NOT NULL,
  user_answer VARCHAR(100) NOT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY(question_id) REFERENCES quiz_question (id),
  FOREIGN KEY(user_id) REFERENCES user (id)
);
