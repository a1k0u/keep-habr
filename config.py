import logging
import os

logging.basicConfig(
    filename="logger.log",
    format="%(asctime)s %(levelname)s in %(module)s with message: '%(message)s'",
    level="NOTSET",
)

logger = logging.getLogger("habr")


api_url = os.getenv("TELEGRAM_URL")
api_token = os.getenv("TELEGRAM_TOKEN")
server_url = os.getenv("SERVER_URL")

bot_access = f"{api_url}{api_token}"

title_pattern = "(?<=\<span\>)[а-яА-Я\w\!\"\#\$\%\&\'\(\)\*\+\,\-\.\/\:\;\<\=\>\?\@\[\]\^\`\{\|\}\~\\\ ]*(?=\<\/span\>\<\/h1\>)"
url_pattern = r"(?<=https\:\/\/habr.com\/)[\w\-\&\=\:\?\/\.]*(?=)"

head = r"(?=\<head\ \>)[\s\S\w\W]*(?=\<\/head\>)"
title = r"(?<=\<title\>)[\s\S\w\Wа-яА-Я]*(?=\<\/title\>)"

db_name = "habr.db"

if __name__ == "__main__":
    print(
        "".join(
            [
                f"{var} = {value}\n"
                for var, value in locals().items()
                if not var.startswith("__")
            ]
        )
    )

    logger.debug("Printed all local variables in config.py!")
