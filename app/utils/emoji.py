def get_emoji_number(number: int) -> str:
    """Returns list of emoji unicodes by number"""

    numbers = {
        "0": "\U00000030\U0000FE0F\U000020E3",
        "1": "\U00000031\U0000FE0F\U000020E3",
        "2": "\U00000032\U0000FE0F\U000020E3",
        "3": "\U00000033\U0000FE0F\U000020E3",
        "4": "\U00000034\U0000FE0F\U000020E3",
        "5": "\U00000035\U0000FE0F\U000020E3",
        "6": "\U00000036\U0000FE0F\U000020E3",
        "7": "\U00000037\U0000FE0F\U000020E3",
        "8": "\U00000038\U0000FE0F\U000020E3",
        "9": "\U00000039\U0000FE0F\U000020E3",
    }

    return "".join([numbers[el] for el in str(number)])
