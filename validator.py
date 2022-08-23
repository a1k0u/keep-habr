from typing import Tuple


def validate(msg: dict) -> Tuple[int, str]:
    if msg.get("text", None) is None:
        return 404, u"Отправьте, пожалуйста, ссылку на пост \U0001F972"

    text = msg["text"]
    

