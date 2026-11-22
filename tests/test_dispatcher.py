import unittest
from unittest.mock import MagicMock

from bot.dispatcher import Dispatcher
from bot.handlers.base import Handler, HandlerStatus


class TestDispatcher(unittest.TestCase):
    def test_stops_on_stop_status(self) -> None:
        handler1 = MagicMock(spec=Handler)
        handler1.handle.return_value = HandlerStatus.STOP
        handler2 = MagicMock(spec=Handler)
        dispatcher = Dispatcher([handler1, handler2])
        dispatcher.dispatch({})
        handler1.handle.assert_called_once()
        handler2.handle.assert_not_called()
