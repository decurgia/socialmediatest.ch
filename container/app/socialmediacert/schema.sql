DROP TABLE IF EXISTS certificate;
DROP TABLE IF EXISTS question;

CREATE TABLE certificate (
  email_hash TEXT PRIMARY KEY,
  valid_until TEXT NOT NULL
);

CREATE TABLE question (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  question TEXT NOT NULL,
  option1 TEXT,
  option2 TEXT,
  option3 TEXT,
  option4 TEXT,
  answer TEXT
);

INSERT INTO question 