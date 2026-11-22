from typing import Any

from ..messenger import Messenger
from .base import Handler, HandlerStatus


class MessageTextHandler(Handler):
    def __init__(self, messenger: Messenger) -> None:
        self.messenger = messenger

    def handle(self, update: dict[str, Any]) -> HandlerStatus:
        message = update.get("message", {})
        text = message.get("text")
        if not text:
            return HandlerStatus.CONTINUE
        chat_id = message["chat"]["id"]
        self.messenger.send_message(chat_id, text)
        return HandlerStatus.STOP
