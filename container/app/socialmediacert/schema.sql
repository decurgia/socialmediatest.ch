DROP TABLE IF EXISTS test;
DROP TABLE IF EXISTS question;
DROP TABLE IF EXISTS certificate;

CREATE TABLE test (
  test_id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  short_description TEXT NOT NULL,
  description TEXT NOT NULL,
  number_of_questions INTEGER NOT NULL DEFAULT 10,
  pass_quota REAL NOT NULL DEFAULT 1.00
);

CREATE TABLE question (
  question_id INTEGER PRIMARY KEY AUTOINCREMENT,
  question_test INTEGER NOT NULL,
  question TEXT NOT NULL,
  option1 TEXT NOT NULL,
  option2 TEXT NOT NULL,
  option3 TEXT,
  option4 TEXT,
  answer INTEGER NOT NULL,
  FOREIGN KEY(question_test) REFERENCES test(test_id)
);

CREATE TABLE certificate (
  email_hash TEXT NOT NULL,
  certificate_test INTEGER NOT NULL,
  valid_until DATE NOT NULL,
  FOREIGN KEY(certificate_test) REFERENCES test(test_id),
  PRIMARY KEY (email_hash, certificate_test)
);

CREATE INDEX "email_hash" ON "certificate" (
	"email_hash"
);