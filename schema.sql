DROP TABLE post;
DROP TABLE user_post;

CREATE TABLE IF NOT EXISTS post (
  id INTEGER PRIMARY KEY AUTOINCREMENT ,
  title TEXT NOT NULL,
  url TEXT(300) NOT NULL UNIQUE,
  count INTEGER
);

CREATE TABLE IF NOT EXISTS user_post (
    chat_id INTEGER NOT NULL,
    post_id INTEGER,
    FOREIGN KEY (post_id) REFERENCES post(id)
);
