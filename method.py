import re
import string


from typing import List
from typing import Tuple

import requests

from config import api_url
from config import api_token
from config import server_url


Post = Tuple[str, str]
Code = int


def get_posts(msg: dict) -> Tuple[Code, List[Post]]:
    text = msg["text"]
    entities = msg["entities"]
    posts = []

    for entity in entities:
        _type = entity["type"]
        start_pos = entity["offset"]
        end_pos = start_pos + entity["length"]

        if _type == "url":
            url_pattern = r"(?<=https\:\/\/habr.com\/)[\w\-\&\=\:\?\/\.]*(?=)"
            url = text[start_pos:end_pos]

            if not re.findall(url_pattern, url):
                continue

            title_pattern = r"(?<=<h1\ data\-test\-id\=\"articleTitle\"\ class=\"tm\-article\-snippet\_\_title\ " \
                            r"tm\-article\-snippet\_\_title\_h1\"\ lang\=\"ru\"\>\<span\>)[а-яА-Я\w\!\"\#\$\%\&\'\(" \
                            r"\)\*\+\,\-\.\/\:\;\<\=\>\?\@\[\]\^\_\`\{\|\}\~\\\ ]*(?=\<\/span\>\<\/h1\>) "
            title = re.findall(title_pattern, requests.get(url).content.decode("utf-8"))

            posts.append((title, url))

        elif _type == "text_link":
            title = text[start_pos:end_pos]
            url = entity["url"]

            posts.append((title, url))

    if not posts:
        return 404, ...

    return 200, posts


def send_message(chat_id: int, text: str) -> int:
    url: str = f"{api_url}{api_token}/sendMessage"
    data = {"chat_id": chat_id, "text": text}

    requests.post(url, data=data)

    return 200


def send_posts(chat_id: str):
    ...


def delete_post(chat_id: str, post_id: str):
    ...


def set_webhook() -> None:
    url: str = f"{api_url}{api_token}/setWebhook"
    response = requests.get(url, params={"url": server_url})
    print(f"Set webhook: {response.status_code}")


def delete_webhook() -> None:
    url: str = f"{api_url}{api_token}/deleteWebhook"
    response = requests.get(url)
    print(f"Delete webhook: {response.status_code}")
