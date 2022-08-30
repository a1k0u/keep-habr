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

title_pattern = (
    r"(?<=\<span\>)[а-яА-Я\w\!\"\#\$\%\&\'\(\)\*\+\,\-\.\/\:\;\<\=\>\?\@\[\]\^\`\{\|\}\~\\\ ]*("
    r"?=\<\/span\>\<\/h1\>) "
)
url_pattern = r"(?<=https\:\/\/habr.com\/)[\w\-\&\=\:\?\/\.]*(?=)"

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
