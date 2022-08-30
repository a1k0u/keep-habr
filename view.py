from typing import Union
import json

from flask import request, Response
from flask import jsonify
from flask import Response
import requests

from app import app
from method import send_message
from method import get_posts
from method import send_posts
from validator import validate_msg
import config as c


@app.route("/", methods=["POST"])
def process() -> Response:
    """

    :return:
    """

    update = request.json

    with open("a.json", "w") as f:
        f.write(json.dumps(update, indent=4))

    msg = update.get("message", None)
    if msg:
        chat_id = msg["chat"]["id"]
        code, message = validate_msg(msg)

        if code == 404:
            return jsonify(dict(code=send_message(chat_id, message)))

        code, posts = get_posts(msg)
        if code == 404:
            return jsonify(
                dict(code=send_message(chat_id, "Ссылки на Хабр? Не, не слышал.."))
            )

        send_message(
            chat_id, text=f"\n".join([f"{i}. [{value[0]}]({value[1]})" for i, value in enumerate(posts)])
        )
        message_id = msg["message_id"]
        requests.post(
            f"{c.api_url}{c.api_token}/deleteMessage",
            data={"chat_id": chat_id, "message_id": message_id},
        )
        # requests.post(f"{c.api_url}{c.api_token}/answerCallbackQuery",
        #               data={"callback_query_id": chat_id, "text": "ok", "show_alert": True})

    return jsonify(dict(code=200))
