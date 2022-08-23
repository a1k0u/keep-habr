import json

import requests
from flask import request
from app import app
from method import send_message


@app.route("/", methods=["POST"])
def get_post():
    update = request.json
    msg = update.get("message", None)

    with open("a.json", "w") as f:
        f.write(json.dumps(update, indent=4))

    if msg:
        chat_id = msg["chat"]["id"]
        message = "sddfssdf"
        send_message(chat_id, message)

    return {"code": 200}
