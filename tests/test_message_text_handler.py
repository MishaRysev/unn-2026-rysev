import unittest
from unittest.mock import MagicMock

from bot.handlers.base import HandlerStatus
from bot.handlers.message_text import MessageTextHandler


class TestMessageTextHandler(unittest.TestCase):
    def test_echoes_text(self) -> None:
        messenger = MagicMock()
        handler = MessageTextHandler(messenger)
        update = {"message": {"text": "Hello", "chat": {"id": 123}}}
        status = handler.handle(update)
        self.assertEqual(status, HandlerStatus.STOP)
        messenger.send_message.assert_called_once_with(123, "Hello")

    def test_ignores_non_text(self) -> None:
        handler = MessageTextHandler(MagicMock())
        update = {"message": {"chat": {"id": 123}}}
        status = handler.handle(update)
        self.assertEqual(status, HandlerStatus.CONTINUE)
