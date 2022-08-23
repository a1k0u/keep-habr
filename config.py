import os

api_url = os.getenv("TELEGRAM_URL")
api_token = os.getenv("TELEGRAM_TOKEN")
server_url = os.getenv("SERVER_URL")

title_pattern = r"(?<=\<span\>)[а-яА-Я\w\!\"\#\$\%\&\'\(\)\*\+\,\-\.\/\:\;\<\=\>\?\@\[\]\^\`\{\|\}\~\\\ ]*(?=\<\/span\>\<\/h1\>)"
url_pattern = r"(?<=https\:\/\/habr.com\/)[\w\-\&\=\:\?\/\.]*(?=)"
