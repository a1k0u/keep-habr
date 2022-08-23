"""

"""

from typing import List
from typing import Tuple
import re

import requests

import config as cfg

Post = Tuple[str, str]
Code = int


def get_posts(msg: dict) -> Tuple[Code, List[Post]]:
    """

    :param msg:
    :return:
    """
    text = msg["text"]
    entities = msg["entities"]
    posts = []

    for entity in entities:
        _type = entity["type"]
        start_pos = entity["offset"]
        end_pos = start_pos + entity["length"]

        if _type == "url":
            url = text[start_pos:end_pos]

            if not re.findall(cfg.url_pattern, url):
                continue

            page_content = requests.get(url).content.decode("utf-8")
            title = re.findall(cfg.title_pattern, page_content)

            posts.append((title, url))

        elif _type == "text_link":
            title = text[start_pos:end_pos]
            url = entity["url"]

            posts.append((title, url))

    if not posts:
        return 404, ...

    return 200, posts


def send_message(chat_id: int, text: str) -> int:
    """

    :param chat_id:
    :param text:
    :return:
    """
    url: str = f"{cfg.api_url}{cfg.api_token}/sendMessage"
    data = {"chat_id": chat_id, "text": text}

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
    """

    :return:
    """
    url: str = f"{cfg.api_url}{cfg.api_token}/deleteWebhook"
    response = requests.get(url)
    print(f"Delete webhook: {response.status_code}")
