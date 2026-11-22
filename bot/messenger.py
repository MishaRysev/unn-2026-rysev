from abc import ABC, abstractmethod
from typing import Any


class Messenger(ABC):
    @abstractmethod
    def get_updates(self, offset: int, timeout: int) -> list[dict[str, Any]]:
        pass

    @abstractmethod
    def send_message(self, chat_id: int, text: str) -> None:
        pass
