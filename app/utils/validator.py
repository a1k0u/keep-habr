from typing import Tuple
import app.utils.answer_phrase as phr


def validate_msg(msg: dict) -> Tuple[int, str]:
    """

    :param msg:
    :return:
    """

    if msg.get("text", None) is None:
        return 404, phr.NO_LETTER

    if msg.get("entities", None) is None:

        if msg["text"] == phr.OUTPUT_LINKS_BTN:
            return 201, ...

        return 404, phr.NO_LINKS

    return 200, ...
