import wolframalpha
from watson_developer_cloud import TextToSpeechV1

def returnAPI():
	client = wolframalpha.Client('E4AJTP-KVK8TU6UPG')
	return client

def returnTextToSpeech():
    text_to_speech = TextToSpeechV1(
        iam_apikey='dS8wjELlw67e9OQzuZKaKIrJqNnRb7PegECPwi_KP-OF',
        url='https://stream.watsonplatform.net/text-to-speech/api'
    )
    return text_to_speech
