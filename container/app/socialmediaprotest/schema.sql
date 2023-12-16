DROP TABLE IF EXISTS test;
DROP TABLE IF EXISTS question;
DROP TABLE IF EXISTS certificate;

CREATE TABLE test (
  id INTEGER NOT NULL,
  locale TEXT NOT NULL DEFAULT 'en',
  name TEXT NOT NULL,
  short_description TEXT NOT NULL,
  description TEXT NOT NULL,
  number_of_questions INTEGER NOT NULL DEFAULT 10,
  pass_quota REAL NOT NULL DEFAULT 1.00,
  PRIMARY KEY (id, locale)
);

CREATE TABLE question (
  id INTEGER NOT NULL,
  locale TEXT NOT NULL DEFAULT 'en',
  fk_test_id INTEGER NOT NULL,
  question TEXT NOT NULL,
  option1 TEXT NOT NULL,
  option2 TEXT NOT NULL,
  option3 TEXT,
  option4 TEXT,
  answer INTEGER NOT NULL,
  FOREIGN KEY (fk_test_id) REFERENCES test(id),
  PRIMARY KEY (id, locale, fk_test_id)
);

CREATE TABLE certificate (
  email_hash TEXT NOT NULL,
  fk_test_id INTEGER NOT NULL,
  valid_until DATE NOT NULL,
  FOREIGN KEY (fk_test_id) REFERENCES test(d),
  PRIMARY KEY (email_hash, fk_test_id)
);

CREATE INDEX "email_hash" ON "certificate" (
	"email_hash"
);

CREATE INDEX "id_locale" ON "test" (
  "id", 
  "locale"
);