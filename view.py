import json


from flask import request
from flask import jsonify
from flask import Response
import requests

from app import app
from method import send_message
from method import get_posts
from validator import validate_msg
from emoji import get_emoji_from_int
import config as c
import db


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

        if code == 201:
            posts = db.get_user_posts(chat_id)
            print(posts)
            send_message(
                chat_id,
                text=f"\n\n".join(
                    [
                        f"{get_emoji_from_int(i + 1)}\t[{posts[i][3]}]({posts[i][4]})"
                        for i in range(len(posts))
                    ]
                ),
            )

            return jsonify(dict(code=200))

        else:
            code, posts = get_posts(msg)

        if code == 404:
            return jsonify(
                dict(code=send_message(chat_id, "Ссылки на Хабр? Не, не слышал.."))
            )

        for post in posts:
            db.add_post_to_user(chat_id, *post)

        send_message(
            chat_id,
            text="Ага, ссылочки добавил",
            reply_markup=json.dumps({"keyboard": [[{"text": "Вывести все ссылки."}]]}),
        )

        """
        posts_per_page = 5
        amount_posts = len(posts)
        amount_pages = amount_posts // posts_per_page
        current_page = 1
        send_message(
            chat_id,
            text=f"\n\n".join(
                [f"{get_emoji_from_int(i + 1)}\t[{posts[i][0]}]({posts[i][1]})"
                 for i in range((current_page - 1) * posts_per_page, min(current_page * posts_per_page, amount_posts))]),
            reply_markup=json.dumps(
                {
                    "inline_keyboard": [
                        [
                            {"text": f"\U00002039 {(x := current_page - 1)}", "callback_data": x},
                            {"text": f"\U00000387 {current_page} \U00000387", "callback_data": current_page},
                            {"text": f"{(y := current_page + 1)} \U0000203A", "callback_data": y}
                        ]
                    ]
                }
            ),
        )
        
        message_id = msg["message_id"]
        requests.post(
            f"{c.api_url}{c.api_token}/deleteMessage",
            data={"chat_id": chat_id, "message_id": message_id},
        )
        """

        # requests.post(f"{c.api_url}{c.api_token}/answerCallbackQuery",
        #               data={"callback_query_id": chat_id, "text": "ok", "show_alert": True})

    return jsonify(dict(code=200))
