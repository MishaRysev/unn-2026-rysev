from typing import Any

from .messenger import Messenger


class LongPolling:
    def __init__(self, messenger: Messenger, timeout: int = 30) -> None:
        self.messenger = messenger
        self.timeout = timeout
        self.offset = 0

    def poll_once(self) -> list[dict[str, Any]]:
        updates = self.messenger.get_updates(self.offset, self.timeout)
        for update in updates:
            self.offset = max(self.offset, update["update_id"] + 1)
        return updates
