import os
import random
import sys

from dotenv import load_dotenv
import dialogflow_v2 as dialogflow
from vk_api.longpoll import VkLongPoll, VkEventType
import vk_api


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


def reply_to_message(project_id, event, vk_api):
    reply = detect_intent_texts(project_id, event.user_id, event.text)

    vk_api.messages.send(
        user_id=event.user_id,
        message=reply,
        random_id=random.randint(1, 1000)
    )


def main():
    load_dotenv()

    project_id = os.getenv('DIALOGFLOW_PROJECT_ID')
    token = os.getenv('VK_TOKEN')

    vk_session = vk_api.VkApi(token=token)
    api_vk = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            reply_to_message(project_id, event, api_vk)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()
