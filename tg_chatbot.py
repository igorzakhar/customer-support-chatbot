import functools
import logging
import os

import dialogflow_v2 as dialogflow
from log import configure_logger
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import Filters


logger = logging.getLogger(__file__)


def start(bot, update):
    update.message.reply_text('Здравствуйте.')


def detect_intent_texts(project_id, session_id, text, lang_code='ru-RU'):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.types.TextInput(text=text, language_code=lang_code)
    query_input = dialogflow.types.QueryInput(text=text_input)

    response = session_client.detect_intent(
        session=session,
        query_input=query_input
    )

    return response.query_result.fulfillment_text


def reply(bot, update, project_id):
    reply_message = detect_intent_texts(
        project_id,
        update.message.chat_id,
        update.message.text
    )

    update.message.reply_text(reply_message)


def run_chatbot(token, project_id):
    updater = Updater(token)

    dp = updater.dispatcher

    reply_to_message = functools.partial(reply, project_id=project_id)

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text, reply_to_message))

    logger.info(f'Бот "{__file__}" запущен.')

    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


def main():
    logging.basicConfig(level=logging.WARNING)

    tg_token = os.getenv('TELEGRAM_API_TOKEN')
    project_id = os.getenv('DIALOGFLOW_PROJECT_ID')
    logger_bot_token = os.getenv('LOGGER_TOKEN')
    logger_bot_chat_id = os.getenv('LOGGER_CHAT_ID')

    configure_logger(
        __file__,
        level=logging.INFO,
        bot_token=logger_bot_token,
        chat_id=logger_bot_chat_id
    )

    while True:
        try:
            run_chatbot(tg_token, project_id)

        except Exception as err:
            logger.error(f'Бот "{__file__}" упал с ошибкой.')
            logger.exception(err)

            continue


if __name__ == '__main__':
    main()
