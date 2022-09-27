import json
from typing import Tuple

from flask import request, Response
from flask import jsonify
from flask import Response
from flask import Blueprint
import requests

from app.api.method import send_message
from app.api.method import get_posts_from_msg
from app.utils.validator import validate_msg
from app.utils.emoji import get_emoji_number
import app.db.db as db
import app.utils.config as c
import app.utils.answer_phrase as phr
import app.utils.keyboard as keyboard

api = Blueprint("api", __name__)


def __out_put_posts(posts):
    return f"\n\n".join(
        [
            f"{get_emoji_number(i + 1)}\t" 
            f"[{posts[i][3]}]({posts[i][4]})"
            for i in range(len(posts))
        ]
    )


@api.route("/", methods=["POST"])
def process() -> Response:
    """

    :return:
    """

    update = request.json

    with open("last_update.json", "w") as f:
        f.write(json.dumps(update, indent=4))

    msg = update.get("message", None)
    if msg:
        chat_id = msg["chat"]["id"]
        code, message = validate_msg(msg)

        if code == 404:
            send_message(chat_id, message)

        if code == 201:
            posts = db.get_user_posts(chat_id)
            send_message(
                chat_id,
                text=__out_put_posts(posts),
            )

        if code == 200:
            _code, posts = get_posts_from_msg(msg)
            if _code == 404:
                send_message(chat_id, phr.NO_HABR_LINKS)
            else:
                for post in posts:
                    db.add_post_to_user(chat_id, *post)

                send_message(
                    chat_id, text=phr.ADDED_LINKS, reply_markup=keyboard.reply_keyboard
                )

    return jsonify({"msg": "ok"})
