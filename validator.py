from typing import Tuple


def validate_msg(msg: dict) -> Tuple[int, str]:
    """

    :param msg:
    :return:
    """

    if msg.get("text", None) is None:
        return 404, "Я понимаю только буковки \U0001F921"

    if msg.get("entities", None) is None:

        if msg["text"] == "Вывести все ссылки.":
            return 201, ...

        return 404, "Ссылками тут и не пахло \U0001F44F"

    return 200, ...
