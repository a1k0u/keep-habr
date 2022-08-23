from typing import Tuple


def validate_msg(msg: dict) -> Tuple[int, str]:
    if msg.get("text", None) is None:
        return 404, u"Я понимаю только буковки \U0001F921"

    if msg.get("entities", None) is None:
        return 404, u"Ссылками тут и не пахло \U0001F44F"

    return 200, ...
