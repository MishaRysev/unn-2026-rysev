from typing import Any

from .handlers.base import Handler, HandlerStatus


class Dispatcher:
    def __init__(self, handlers: list[Handler]) -> None:
        self.handlers = handlers

    def dispatch(self, update: dict[str, Any]) -> None:
        for handler in self.handlers:
            if handler.handle(update) is HandlerStatus.STOP:
                break
