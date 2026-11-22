import unittest
from unittest.mock import MagicMock

from bot.long_polling import LongPolling


class TestLongPolling(unittest.TestCase):
    def test_poll_once_updates_offset(self) -> None:
        messenger = MagicMock()
        messenger.get_updates.return_value = [{"update_id": 1}, {"update_id": 2}]
        polling = LongPolling(messenger)
        polling.poll_once()
        self.assertEqual(polling.offset, 3)
        messenger.get_updates.assert_called_once_with(0, 30)
