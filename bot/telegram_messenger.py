import json
import os
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, cast

from .messenger import Messenger


class TelegramMessenger(Messenger):
    def __init__(self) -> None:
        raw_base = os.environ.get("TELEGRAM_BASE_URL", "").strip()
        if raw_base and not raw_base.startswith("http"):
            raw_base = "http://" + raw_base
            
        self.base_url = raw_base.rstrip("/")
        self.token = os.environ.get("TELEGRAM_TOKEN", "").strip()

        if not self.base_url or not self.token:
            print("[WARNING] TELEGRAM_BASE_URL или TELEGRAM_TOKEN не заданы!", flush=True)

    def _request(self, method: str, **params: object) -> Any:
        url = f"{self.base_url}/bot{self.token}/{method}"
        print(f"[DEBUG] Отправка запроса на: {url}", flush=True)
        
        request = urllib.request.Request(
            url,
            data=urllib.parse.urlencode(params).encode(),
            method="POST",
        )
        
        poll_timeout = params.get("timeout", 10)
        socket_timeout = (poll_timeout + 15) if isinstance(poll_timeout, int) else 30

        try:
            with urllib.request.urlopen(request, timeout=socket_timeout) as response:
                payload = json.loads(response.read())
        except urllib.error.HTTPError as e:
            payload = json.loads(e.read())
        except Exception as e:
            print(f"[ERROR] Сетевая ошибка: {e}", flush=True)
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