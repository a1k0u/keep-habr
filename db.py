import sqlite3
from typing import Callable
from typing import Union
from typing import Tuple
from typing import Any
from config import db_name


def get_connection() -> sqlite3.Connection:
    return sqlite3.connect(db_name)


def get_cursor(func: Callable) -> Callable:
    """
    Create an instance of connection for database with cursor.
    If no exceptions in wrapped function, changes will commit,
    in another way - rollback.
    """

    def wrapper(*args, **kwargs) -> Any:
        con = get_connection()
        cur = con.cursor()

        res = func(cur, *args, **kwargs)

        con.commit()

        cur.close()
        con.close()

        return res

    return wrapper


def check_connection_user_post(cur: sqlite3.Cursor, chat_id: int, post_id: int) -> int:
    return cur.execute(
        "SELECT * FROM user_post WHERE chat_id = ? AND post_id = ?", (chat_id, post_id)
    ).fetchone()


def connect_user_post(cur: sqlite3.Cursor, chat_id: int, post_id: int) -> None:
    cur.execute(
        "INSERT INTO user_post (chat_id, post_id) VALUES (?, ?)", (chat_id, post_id)
    )


def disconnect_user_post(cur: sqlite3.Cursor, chat_id: int, post_id: int) -> None:
    cur.execute(
        "DELETE FROM user_post WHERE chat_id = ? AND post_id = ?", (chat_id, post_id)
    )


@get_cursor
def get_user_posts(cur: sqlite3.Cursor, chat_id: int):
    return cur.execute(
        """
        SELECT *
        FROM (
            SELECT chat_id, post_id
            FROM user_post 
            WHERE chat_id = ?
        ) AS user
        JOIN post 
        ON post.id = user.post_id
        """,
        (chat_id,)
    ).fetchall()


@get_cursor
def add_post_to_user(cur: sqlite3.Cursor, chat_id: int, title: str, url: str) -> None:
    post_id, count = (
        x if (x := get_post(cur, url)) is not None else insert_post(cur, title, url)
    )

    if count and check_connection_user_post(cur, chat_id, post_id) is not None:
        return

    increment_link_to_post(cur, url, count)

    connect_user_post(cur, chat_id, post_id)


@get_cursor
def delete_post_from_user(cur: sqlite3.Cursor, chat_id: int, url: str) -> None:
    post_info = get_post(cur, url)

    if post_info is None:
        return

    post_id, count = post_info

    decrement_link_to_post(cur, url, count)
    disconnect_user_post(cur, chat_id, post_id)


def get_post(cur: sqlite3.Cursor, url: str) -> Tuple[int, int]:
    """Finds post by url and returns id and amount of links."""
    return cur.execute("SELECT id, count FROM post WHERE url = ?", (url,)).fetchone()


def insert_post(cur: sqlite3.Cursor, title: str, url: str) -> Tuple[int, int]:
    """Creates post in db and returns id and amount of links"""

    cur.execute(
        "INSERT INTO post (title, url, count) VALUES (?, ?, ?)", (title, url, 0)
    )
    return cur.lastrowid, 0


def delete_post(cur: sqlite3.Cursor, url: str) -> None:
    """Delete post by url - identification"""

    cur.execute("DELETE FROM post WHERE url = ?", (url,))


def __update_post_count(cur: sqlite3.Cursor, url: str, count: int) -> None:
    cur.execute("UPDATE post SET count = ? WHERE url = ?", (count, url))


def increment_link_to_post(cur: sqlite3.Cursor, url: str, count: int) -> None:
    """
    Increment amount of links for post.

    :param cur:
    :param url: identification for post
    :param count: amount of links
    """

    __update_post_count(cur, url, count + 1)


def decrement_link_to_post(cur: sqlite3.Cursor, url: str, count: int) -> None:
    """
    Decrement links to post. If amount of link is zero, post will delete

    :param cur:
    :param url: identification for post
    :param count: links for post
    """

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
