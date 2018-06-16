DROP TABLE IF EXISTS author;
DROP TABLE IF EXISTS question;
DROP TABLE IF EXISTS solution;

CREATE TABLE author(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    email TEXT NOT NULL
);

CREATE TABLE question(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT NOT NULL
);

CREATE TABLE solution(
    solution_id INTEGER PRIMARY KEY AUTOINCREMENT,
    author_id INTEGER NOT NULL,
    question_id INTEGER NOT NULL,
    author TEXT NOT NULL,
    language TEXT NOT NULL,
    nickname TEXT NOT NULL,
    complexiry TEXT,
    runtime FLOAT,
    percentage FLOAT,
    interpretation TEXT NULL,
    sourcecode TEXT NOT NULL,
    FOREIGN KEY (author_id) REFERENCES author (id),
    FOREIGN KEY (question_id) REFERENCES question (id)
);