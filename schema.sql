CREATE TABLE role (
	id INTEGER NOT NULL,
	name VARCHAR(80),
	description VARCHAR(255),
	PRIMARY KEY (id),
	UNIQUE (name)
);

CREATE TABLE user (
	id INTEGER NOT NULL,
	email VARCHAR(120) NOT NULL,
	firstname VARCHAR(30) NOT NULL,
	lastname VARCHAR(30) NOT NULL,
	password VARCHAR(255) NOT NULL,
	active BOOLEAN,
	confirmed_at DATETIME,
	PRIMARY KEY (id),
	CHECK (active IN (0, 1))
);

CREATE UNIQUE INDEX ix_user_email ON user (email);
CREATE UNIQUE INDEX ix_user_lastname ON user (lastname);
CREATE UNIQUE INDEX ix_user_firstname ON user (firstname);

CREATE TABLE assignment (
	id INTEGER NOT NULL,
	name VARCHAR(100) NOT NULL,
	description TEXT NOT NULL,
	points INTEGER NOT NULL,
	PRIMARY KEY (id)
);

CREATE UNIQUE INDEX ix_assignment_name ON assignment (name);

CREATE TABLE exercise (
	id INTEGER NOT NULL,
	prompt TEXT NOT NULL,
	hint TEXT NOT NULL,
	test_cases TEXT NOT NULL,
	solution TEXT NOT NULL,
	PRIMARY KEY (id)
);

CREATE TABLE roles_users (
	user_id INTEGER,
	role_id INTEGER,
	FOREIGN KEY(user_id) REFERENCES user (id),
	FOREIGN KEY(role_id) REFERENCES role (id)
);

CREATE TABLE grade (
	id INTEGER NOT NULL,
	score INTEGER NOT NULL,
	user_id INTEGER,
	assignment_id INTEGER,
	PRIMARY KEY (id),
	FOREIGN KEY(user_id) REFERENCES user (id),
	FOREIGN KEY(assignment_id) REFERENCES assignment (id)
);
