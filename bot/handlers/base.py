from abc import ABC, abstractmethod
from enum import Enum
from typing import Any


class HandlerStatus(Enum):
    STOP = "stop"
    CONTINUE = "continue"


class Handler(ABC):
    @abstractmethod
    def handle(self, update: dict[str, Any]) -> HandlerStatus:
        pass
