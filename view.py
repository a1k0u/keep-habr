import requests
from app import app


def send_posts(chat_id: str):
    ...


def delete_post(chat_id: str, post_id: str):
    ...


@app.route("/", methods=["GET", "POST"])
def get_post():
    ...





