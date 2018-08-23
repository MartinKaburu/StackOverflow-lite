CREATE TABLE IF NOT EXISTS users(
  id SERIAL PRIMARY KEY,
username varchar (32) NOT NULL,
email varchar (32) UNIQUE NOT NULL,
password VARCHAR (256) NOT NULL
);

CREATE TABLE IF NOT EXISTS questions(
id SERIAL PRIMARY KEY,
content TEXT NOT NULL,
question_owner INT NOT NULL REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS answers(
id SERIAL PRIMARY KEY,
content TEXT NOT NULL,
answer_owner INT NOT NULL REFERENCES users(id),
upvotes INT DEFAULT 0,
downvotes INT DEFAULT 0,
accepted BOOLEAN DEFAULT FALSE,
question_id INT NOT NULL REFERENCES questions(id)
);

CREATE TABLE IF NOT EXISTS votes(
id SERIAL REFERENCES answers(id),
voter INT NOT NULL REFERENCES users(id)
);
