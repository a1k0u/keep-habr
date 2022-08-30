def get_emoji_from_int(number: int) -> str:
    """Returns list of emoji unicodes by number"""
    numbers = {
        0: "0️⃣",
        1: "1️⃣",
        2: "2️⃣",
        3: "3️⃣",
        4: "4️⃣",
        5: "5️⃣",
        6: "6️⃣",
        7: "7️⃣",
        8: "8️⃣",
        9: "9️⃣",
    }

    return "".join([numbers[int(el)] for el in str(number)])
