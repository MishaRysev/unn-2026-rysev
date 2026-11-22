import json
import os
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, cast

from .messenger import Messenger


class TelegramMessenger(Messenger):
    def __init__(self) -> None:
        self.base_url = os.environ["TELEGRAM_BASE_URL"]
        self.token = os.environ["TELEGRAM_TOKEN"]

    def _request(self, method: str, **params: object) -> Any:
        base = self.base_url.rstrip("/")
        url = f"{base}/bot{self.token}/{method}"
        
        request = urllib.request.Request(
            url,
            data=urllib.parse.urlencode(params).encode(),
            method="POST",
        )

        opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
        
        print(f"[DEBUG] Отправка запроса на: {url}")
        
        try:
            with opener.open(request, timeout=10) as response:
                payload = json.loads(response.read())
        except urllib.error.HTTPError as e:
            payload = json.loads(e.read())
        except urllib.error.URLError as e:
            print(f"[ERROR] Ошибка соединения: {e.reason}")
            raise

        if not payload.get("ok"):
            raise RuntimeError(payload.get("description", "Unknown Telegram API error"))
            
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