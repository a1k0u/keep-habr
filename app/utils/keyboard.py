reply_keyboard = (
    json.dumps(
        {
            "resize_keyboard": True,
            "keyboard": [[{"text": phr.OUTPUT_LINKS_BTN}]],
        }
    ),
)
