import logging
import os
import random
import sys

from dialogflow_tools import detect_intent_texts
from dotenv import load_dotenv
from log import configure_logger
from vk_api.longpoll import VkLongPoll, VkEventType
import vk_api


logger = logging.getLogger(__file__)


def reply_to_message(project_id, event, vk_api):
    reply = detect_intent_texts(project_id, event.user_id, event.text)

    if reply:
        vk_api.messages.send(
            user_id=event.user_id,
            message=reply,
            random_id=random.randint(1, 1000)
        )


def run_chatbot(token, project_id):
    vk_session = vk_api.VkApi(token=token)
    api_vk = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    logger.info(f'Бот "{__file__}" запущен.')

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            reply_to_message(project_id, event, api_vk)


def main():
    load_dotenv()
    logging.basicConfig(level=logging.WARNING)

    project_id = os.getenv('DIALOGFLOW_PROJECT_ID')
    vk_token = os.getenv('VK_TOKEN')
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
            run_chatbot(vk_token, project_id)

        except Exception as err:
            logger.error(f'Бот "{__file__}" упал с ошибкой.')
            logger.exception(err)

            continue


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()
