"""

"""

import re
import json

from typing import List
from typing import Any
from typing import Tuple

import requests

import app.utils.config as cfg
from app.utils.config import logger

Post = Tuple[str, str]
Code = int


def get_posts_from_msg(msg: dict) -> Tuple[int, List[Post] or None]:
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

        _head = re.findall(cfg.head, page_content)
        _title = re.findall(cfg.title, *_head)

        posts.append((*_title, url))

    if not posts:
        return 404, ...

    return 200, posts


def send_message(chat_id: int, text: str, **kwargs) -> Code:
    """

    :param chat_id:
    :param text:
    :return:
    """

    url: str = f"{cfg.bot_access}/sendMessage"
    data = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
    data.update(kwargs)
    print(data)
    print(kwargs)

    requests.post(url, data=data)

    return 200


def send_posts(*args, **kwargs):
    ...


def delete_post(*args, **kwargs):
    ...


def set_webhook() -> None:
    """Set webhook on your sever"""

    url: str = f"{cfg.bot_access}/setWebhook"
    requests.get(url, params={"url": cfg.server_url})

    logger.debug(f"Set webhook on {cfg.server_url}")


def delete_webhook() -> None:
    """Deletes webhook from your server"""

    url: str = f"{cfg.bot_access}/deleteWebhook"
    response = requests.get(url)

    logger.debug(f"Delete webhook: {response.status_code}")
