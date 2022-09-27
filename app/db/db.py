"""
All functions for work with database.
Check docstring, signature of functions and tests.
"""

import sqlite3

from typing import Callable
from typing import Union
from typing import Tuple
from typing import Any

from app.utils.config import db_name
from app.utils.config import logger


def get_connection() -> sqlite3.Connection:
    """Gets instance of connection to db."""
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

        res = None

        try:
            res = func(cur, *args, **kwargs)
        except sqlite3.DatabaseError as e:
            logger.critical(f"Rollback - {func.__name__}. Exception in db - {e}!")
            con.rollback()
        else:
            con.commit()

        cur.close()
        con.close()

        return res

    return wrapper


def __check_connection_user_post(
    cur: sqlite3.Cursor, chat_id: int, post_id: int
) -> Union[int, None]:
    """
    Checks connection between user and post, if for user with
    `chat_id` doesn't exist `url` None will return.
    In opposite case `chat_id` will return.
    """

    return cur.execute(
        "SELECT chat_id FROM user_post WHERE chat_id = ? AND post_id = ?",
        (chat_id, post_id),
    ).fetchone()


def connect_user_post(cur: sqlite3.Cursor, chat_id: int, post_id: int) -> None:
    """Create connection between user and post."""

    cur.execute(
        "INSERT INTO user_post (chat_id, post_id) VALUES (?, ?)", (chat_id, post_id)
    )


def disconnect_user_post(cur: sqlite3.Cursor, chat_id: int, post_id: int) -> None:
    """Deletes row with data or disconnect user (chat_id) and post (url)."""

    cur.execute(
        "DELETE FROM user_post WHERE chat_id = ? AND post_id = ?", (chat_id, post_id)
    )


@get_cursor
def get_user_posts(cur: sqlite3.Cursor, chat_id: int):
    """
    Strategy one to many, gets all posts for exact user.
    """

    logger.debug("In process to return user posts.")

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
        ORDER BY post.title DESC
        """,
        (chat_id,),
    ).fetchall()


@get_cursor
def add_post_to_user(cur: sqlite3.Cursor, chat_id: int, title: str, url: str) -> None:
    """
    Gets or creates post. Post duplicates for user is skipped.
    """

    post_id, count = (
        x if (x := get_post(cur, url)) is not None else insert_post(cur, title, url)
    )

    if count and __check_connection_user_post(cur, chat_id, post_id) is not None:
        logger.debug(f"Post = {post_id} have already added for {chat_id}.")
        return

    increment_link_to_post(cur, url, count)

    connect_user_post(cur, chat_id, post_id)

    logger.debug(f"Add post for user = {chat_id}.")


@get_cursor
def delete_post_from_user(cur: sqlite3.Cursor, chat_id: int, url: str) -> None:
    """
    Gets post if exists, decrements links to it
    and disconnects from user.
    """

    post_info = get_post(cur, url)

    if post_info is None:
        logger.debug("Deleted post isn't exist.")
        return

    post_id, count = post_info

    decrement_link_to_post(cur, url, count)
    disconnect_user_post(cur, chat_id, post_id)

    logger.debug(f"Post was delete from user = {chat_id}.")


def get_post(cur: sqlite3.Cursor, url: str) -> Union[Tuple[int, int], None]:
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


def __update_post_link_count(cur: sqlite3.Cursor, url: str, count: int) -> None:
    cur.execute("UPDATE post SET count = ? WHERE url = ?", (count, url))


def increment_link_to_post(cur: sqlite3.Cursor, url: str, count: int) -> None:
    """Increment amount of links for post."""

    __update_post_link_count(cur, url, count + 1)


def decrement_link_to_post(cur: sqlite3.Cursor, url: str, count: int) -> None:
    """
    Decrement links to post.
    If amount of link is zero, post will delete.
    """

    if not (new_value := count - 1):
        delete_post(cur, url)
    else:
        __update_post_link_count(cur, url, new_value)


@get_cursor
def create_table(cur: sqlite3.Cursor) -> None:
    """Creates tables in database and checks existing of it by assert."""

    with open("schema.sql", mode="r", encoding="utf-8") as schema:
        cur.executescript(schema.read())

    assert {
        el[0] for el in cur.execute("SELECT name FROM sqlite_master").fetchall()
    }.issuperset({"post", "user_post"})

    logger.debug("Tables was created!")


if __name__ == "__main__":
    # Creates a database file and fills it with tables from schema.sql

    import os.path

    if not os.path.exists(db_name):
        open(db_name, mode="w", encoding="utf-8").close()
        logger.debug("File of database was created.")

    create_table()
