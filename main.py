from bot.dispatcher import Dispatcher
from bot.handlers.base import Handler
from bot.handlers.message_text import MessageTextHandler
from bot.long_polling import LongPolling
from bot.telegram_messenger import TelegramMessenger


def main() -> None:
    messenger = TelegramMessenger()
    polling = LongPolling(messenger)
    handlers: list[Handler] = [MessageTextHandler(messenger)]
    dispatcher = Dispatcher(handlers)

    while True:
        updates = polling.poll_once()
        for update in updates:
            dispatcher.dispatch(update)


if __name__ == "__main__":
    main()
