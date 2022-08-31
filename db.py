import sqlite3
from typing import Callable
from typing import Union
from typing import Tuple
from config import db_name


def get_connection() -> sqlite3.Connection:
    return sqlite3.connect(db_name)


def get_cursor(func: Callable) -> Callable:
    def wrapper(*args, **kwargs):
        con = get_connection()
        cur = con.cursor()
        res = None

        try:
            res = func(cur, *args, **kwargs)
        except:
            con.rollback()
        else:
            con.commit()

        cur.close()
        con.close()

        return res

    return wrapper


def get_user_by_post(cur: sqlite3.Cursor, post_id: int) -> int:
    return cur.execute("SELECT chat_id FROM user_post WHERE post_id = ?", (post_id,)).fetchone()


def connect_user_post(cur: sqlite3.Cursor, chat_id: int, post_id: int) -> None:
    cur.execute("INSERT INTO user_post (chat_id, post_id) VALUES (?, ?)", (chat_id, post_id))


def disconnect_user_post(cur: sqlite3.Cursor, chat_id: int, post_id: int) -> None:
    cur.execute("DELETE FROM user_post WHERE chat_id = ? AND post_id = ?", (chat_id, post_id))


@get_cursor
def add_post_to_user(cur: sqlite3.Cursor, chat_id: int, title: str, url: str) -> None:
    post_id, count = x if (x := get_post(cur, url)) is not None else insert_post(cur, title, url)

    increment_link_to_post(cur, url, count)

    if get_user_by_post(cur, post_id) is not None:
        return ...
    connect_user_post(cur, chat_id, post_id)


@get_cursor
def delete_post_from_user(cur: sqlite3.Cursor, chat_id: int, url: str) -> None:
    post_id, count = get_post(cur, url)
    decrement_link_to_post(cur, url, count)

    disconnect_user_post(cur, chat_id, post_id)


def get_post(cur: sqlite3.Cursor, url: str) -> Tuple[int, int]:
    res = cur.execute("SELECT id, count FROM post WHERE url = ?", (url,)).fetchone()
    return res


def insert_post(cur: sqlite3.Cursor, title: str, url: str) -> Tuple[int, int]:
    cur.execute("INSERT INTO post (title, url, count) VALUES (?, ?, ?)", (title, url, 0))
    return cur.lastrowid, 0


def delete_post(cur: sqlite3.Cursor, url: str) -> None:
    cur.execute("DELETE FROM post WHERE url = ?", (url,))


def __update_post_count(cur: sqlite3.Cursor, url: str, count: int) -> None:
    cur.execute("UPDATE post SET count = ? WHERE url = ?", (count, url))


def increment_link_to_post(cur: sqlite3.Cursor, url: str, count: int) -> None:
    __update_post_count(cur, url, count + 1)


def decrement_link_to_post(cur: sqlite3.Cursor, url: str, count: int) -> None:
    if not (new_value := count - 1):
        delete_post(cur, url)
    else:
        __update_post_count(cur, url, new_value)


@get_cursor
def create_table(cur: sqlite3.Cursor) -> None:
    with open("schema.sql", mode="r", encoding="utf-8") as schema:
        cur.executescript(schema.read())

    assert {
        el[0] for el in cur.execute("SELECT name FROM sqlite_master").fetchall()
    }.issuperset({"post", "user_post"})


if __name__ == "__main__":
    # Creates a database file and fills it with tables from schema.sql

    import os.path

    if not os.path.exists(db_name):
        open(db_name, mode="w").close()
    create_table()

    add_post_to_user(12, "e", "d")
