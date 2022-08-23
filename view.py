import json
from typing import Union

import requests
from flask import request, Response
from flask import jsonify
from flask import Response

from app import app
from method import send_message
from method import get_posts
from validator import validate_msg


@app.route("/", methods=["POST"])
def process() -> Union[int, Response]:
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
            return jsonify(dict(code=send_message(chat_id, "Ссылки на Хабр? Не, не слышал..")))

        print(posts)

    return jsonify(dict(code=200))