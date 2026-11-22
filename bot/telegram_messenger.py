import json
import os
import urllib.parse
import urllib.request
from typing import Any, cast

from .messenger import Messenger


class TelegramMessenger(Messenger):
    def __init__(self) -> None:
        self.base_url = os.environ["TELEGRAM_BASE_URL"]
        self.token = os.environ["TELEGRAM_TOKEN"]

    def _request(self, method: str, **params: object) -> Any:
        url = f"{self.base_url}/bot{self.token}/{method}"
        request = urllib.request.Request(
            url,
            data=urllib.parse.urlencode(params).encode(),
            method="POST",
        )
        with urllib.request.urlopen(request) as response:
            payload = json.loads(response.read())
        if not payload["ok"]:
            raise RuntimeError(payload["description"])
        return payload["result"]

    def get_updates(self, offset: int, timeout: int) -> list[dict[str, Any]]:
        result = self._request(
            "getUpdates",
            offset=offset,
            timeout=timeout,
            allowed_updates=json.dumps(["message"]),
        )
        return cast(list[dict[str, Any]], result)

    def send_message(self, chat_id: int, text: str) -> None:
        self._request("sendMessage", chat_id=chat_id, text=text)
