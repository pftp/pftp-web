CREATE TABLE user (
        id INTEGER NOT NULL,
        email VARCHAR(120) NOT NULL,
        firstname VARCHAR(30) NOT NULL,
        lastname VARCHAR(30) NOT NULL,
        role SMALLINT NOT NULL,
        PRIMARY KEY (id)
);

CREATE UNIQUE INDEX ix_user_email ON user (email);
CREATE UNIQUE INDEX ix_user_lastname ON user (lastname);
CREATE UNIQUE INDEX ix_user_firstname ON user (firstname);

CREATE TABLE exercise (
        id INTEGER NOT NULL,
        prompt TEXT NOT NULL,
        hint TEXT NOT NULL,
        test_cases TEXT NOT NULL,
        solution TEXT NOT NULL,
        PRIMARY KEY (id)
);
