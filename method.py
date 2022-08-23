import requests

from config import api_url
from config import api_token
from config import server_url


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
