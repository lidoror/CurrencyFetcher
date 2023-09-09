import json
import os
import telebot
from currency_fetcher.currency import currency_api
from currency_fetcher.log_factory import logger


class Bot:

    def __init__(self, token):
        self.bot = telebot.TeleBot(token)
        self.bot.set_update_listener(self.internal_message_handler)

        self.current_message = None

    def send_message_to_users(self, message: str, chat_ids: list[str] = None) -> None:
        if chat_ids is None:
            chat_ids = json.loads(os.environ.get("CHAT_IDS"))

        for chat_id in chat_ids:
            self.sent_text_by_chat_id(chat_id=chat_id, text=message)

    def internal_message_handler(self, messages) -> None:
        for message in messages:
            logger.info(f'handling message: [{message.text}] ')

            self.current_message = message
            self.handle_message(message)

    def handle_message(self, message) -> None:
        if message.text == 'status':
            status = self.get_currency_account_status()
            self.send_text(status)

    def sent_text_by_chat_id(self, chat_id: str | list[str], text: str) -> None:
        self.bot.send_message(chat_id=chat_id, text=text)

    def send_text(self, text: str):
        self.bot.send_message(self.current_message.chat.id, text)

    def start_bot(self):
        logger.info('_____bot_starting_____')
        self.bot.infinity_polling()

    def notify_exchange_rate(self):
        logger.info('fetching exchange rate')
        url = os.environ.get('EXCHANGE_URL')

        if url is None:
            logger.error('exchange account status was None instead of dict')
            raise ValueError('expected dictionary but got None')

        exchange_rate = currency_api.CurrencyFetcher(url).get_currency_exchange_rate()
        self.send_text(exchange_rate)

    def get_currency_account_status(self) -> str:
        logger.info('bot checking account status')
        url = os.environ.get('STATUS_URL')

        if url is None:
            logger.error('exchange account status was None instead of dict')
            raise ValueError('expected dictionary but got None')

        status = currency_api.CurrencyFetcher(url).get_account_status()
        return status

    def get_exchange_rate(self) -> str:
        logger.info('checking exchange rate')
        url = os.environ.get('EXCHANGE_URL')

        if url is None:
            logger.error('exchange account status was None instead of dict')
            raise ValueError('expected dictionary but got None')

        exchange_rate = currency_api.CurrencyFetcher(url).get_currency_exchange_rate()
        return exchange_rate
