def get_emoji_from_int(number: int) -> str:
    """Returns list of emoji unicodes by number"""
    numbers = {
        "0": u"\U00000030\U0000FE0F\U000020E3",
        "1": u"\U00000031\U0000FE0F\U000020E3",
        "2": u"\U00000032\U0000FE0F\U000020E3",
        "3": u"\U00000033\U0000FE0F\U000020E3",
        "4": u"\U00000034\U0000FE0F\U000020E3",
        "5": u"\U00000035\U0000FE0F\U000020E3",
        "6": u"\U00000036\U0000FE0F\U000020E3",
        "7": u"\U00000037\U0000FE0F\U000020E3",
        "8": u"\U00000038\U0000FE0F\U000020E3",
        "9": u"\U00000039\U0000FE0F\U000020E3",
    }

    return "".join([numbers[el] for el in str(number)])
