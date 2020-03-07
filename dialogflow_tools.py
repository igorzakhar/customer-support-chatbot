import dialogflow_v2 as dialogflow


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
