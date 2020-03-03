import logging

import telegram


class TelegramLogsHandler(logging.Handler):

    def __init__(self, bot_token, chat_id):
        super().__init__()
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.bot = telegram.Bot(token=self.bot_token)

    def emit(self, record):
        log_entry = self.format(record)
        self.bot.send_message(chat_id=self.chat_id, text=log_entry)


def configure_logger(logger_name,
                     level=logging.DEBUG, bot_token=None, chat_id=None):
    logger = logging.getLogger(logger_name)
    logger.setLevel(level)

    if bot_token and chat_id:
        tg_logs_handler = TelegramLogsHandler(bot_token, chat_id)
        log_format = logging.Formatter('%(message)s')
        tg_logs_handler.setFormatter(log_format)
        logger.addHandler(tg_logs_handler)
