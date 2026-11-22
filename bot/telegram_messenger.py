import json
import os
import ssl
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, cast

from .messenger import Messenger


class TelegramMessenger(Messenger):
    def __init__(self) -> None:
        raw_base = os.environ.get("TELEGRAM_BASE_URL", "").strip()

        if raw_base and not raw_base.startswith(("http://", "https://")):
            raw_base = "https://" + raw_base

        if "localhost" in raw_base:
            raw_base = raw_base.replace("localhost", "172.17.0.1")
        elif "127.0.0.1" in raw_base:
            raw_base = raw_base.replace("127.0.0.1", "172.17.0.1")

        self.base_url = raw_base.rstrip("/")
        self.token = os.environ.get("TELEGRAM_TOKEN", "").strip()

    def _request(self, method: str, **params: object) -> Any:
        url = f"{self.base_url}/bot{self.token}/{method}"

        request = urllib.request.Request(
            url,
            data=urllib.parse.urlencode(params).encode(),
            method="POST",
        )

        poll_timeout = params.get("timeout", 10)
        socket_timeout = (poll_timeout + 15) if isinstance(poll_timeout, int) else 30

        context = ssl._create_unverified_context()

        try:
            with urllib.request.urlopen(
                request, timeout=socket_timeout, context=context
            ) as response:
                payload = json.loads(response.read())
        except urllib.error.HTTPError as e:
            payload = json.loads(e.read())
        except Exception as e:
            print(f"[ERROR] Сетевая ошибка при запросе на {url}: {e}", flush=True)
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
