"""

"""
import json
from typing import List, Tuple, Any
from typing import Tuple
import re
import string

import requests

import config as cfg

Post = Tuple[str, str]
Code = int


def get_posts(msg: dict) -> Tuple[int, List[Post] or None]:
    """

    :param msg:
    :return:
    """

    text = msg["text"]
    entities = msg["entities"]
    posts = []

    for entity in entities:
        _type = entity["type"]

        if _type not in ("url", "text_link"):
            continue

        url: str = (
            entity["url"]
            if _type == "text_link"
            else text[(x := entity["offset"]): x + entity["length"]]
        )

        if not re.findall(cfg.url_pattern, url):
            continue

        page_content = requests.get(url).content.decode("utf-8")
        title = re.findall(cfg.title_pattern, page_content)

        print(title)

        posts.append((title, url))

    if not posts:
        return 404, ...

    return 200, posts


def send_message(chat_id: int, text: str = "", dct=None) -> int:
    """

    :param dct:
    :param chat_id:
    :param text:
    :return:
    """

    if dct is None:
        dct = {}

    url: str = f"{cfg.api_url}{cfg.api_token}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown",
        "reply_markup": json.dumps(
            {
                "keyboard": [["Yes", "No"], ["Maybe"], ["1", "2", "3"]],
                "one_time_keyboard": False,
            }
        ),
    }

    print(data)

    requests.post(url, data=data)

    return 200


def send_posts(chat_id: str):
    """

    :param chat_id:
    :return:
    """
    ...


def delete_post(chat_id: str, post_id: str):
    """

    :param chat_id:
    :param post_id:
    :return:
    """
    ...


def set_webhook() -> None:
    """

    :return:
    """
    url: str = f"{cfg.api_url}{cfg.api_token}/setWebhook"
    response = requests.get(url, params={"url": cfg.server_url})
    print(f"Set webhook: {response.status_code}")


def delete_webhook() -> None:
    """Deletes webhook from your server"""

    url: str = f"{cfg.api_url}{cfg.api_token}/deleteWebhook"
    response = requests.get(url)

    print(f"Delete webhook: {response.status_code}")
