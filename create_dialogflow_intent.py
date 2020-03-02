import argparse
import json
import logging
import os
import sys

from dotenv import load_dotenv
import dialogflow_v2 as dialogflow
from google.api_core.exceptions import InvalidArgument


def load_training_phrases(filepath):
    try:
        with open(filepath, 'r') as fp:
            return json.load(fp)
    except OSError as err:
        logging.exception(err, exc_info=False)
        raise


def create_intent(
        project_id, display_name, training_phrases_parts, message_texts):

    intents_client = dialogflow.IntentsClient()

    parent = intents_client.project_agent_path(project_id)
    training_phrases = []

    for training_phrases_part in training_phrases_parts:
        part = dialogflow.types.Intent.TrainingPhrase.Part(
            text=training_phrases_part)

        training_phrase = dialogflow.types.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.types.Intent.Message.Text(text=message_texts)
    message = dialogflow.types.Intent.Message(text=text)

    intent = dialogflow.types.Intent(
        display_name=display_name,
        training_phrases=training_phrases,
        messages=[message])

    response = intents_client.create_intent(parent, intent)

    logging.debug(f'Intent "{response.display_name}" created.')


def process_args():
    parser = argparse.ArgumentParser(
        description='Create archive with user files and download it on demand.'
    )
    parser.add_argument(
        '-p', '--path', required=True, help='Path to training phrases file.'
    )

    return parser.parse_args()


def main():
    load_dotenv()

    logging.getLogger('google.auth.transport.requests').setLevel(
        logging.WARNING
    )
    logging.getLogger('urllib3.connectionpool').setLevel(logging.WARNING)
    logging.basicConfig(level=logging.DEBUG, format='%(message)s')

    project_id = os.getenv('DIALOGFLOW_PROJECT_ID')
    args = process_args()

    training_phrases = load_training_phrases(args.path)

    for intent_name, content in training_phrases.items():
        questions = content['questions']
        answer = content['answer']

        try:
            create_intent(project_id, intent_name, questions, [answer])
        except InvalidArgument as err:
            logging.exception(err.message, exc_info=False)


if __name__ == '__main__':
    try:
        main()
    except OSError:
        sys.exit()
