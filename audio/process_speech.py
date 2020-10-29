import io
import os
from google.cloud import speech
from nltk.corpus import stopwords

client = speech.SpeechClient()
stops = stopwords.words('english')


def ProcessSpeech(filename):
    print("AUDIO SPEECH TO TEXT", filename)
    with io.open(filename, mode='rb') as audio:
        content = audio.read()
        audio = speech.RecognitionAudio(content=content)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=44100,
        language_code="en-US",
        enable_word_time_offsets=True
    )

    request = client.long_running_recognize(config=config, audio=audio)
    print('AWAITING API RESPONSE')
    result = request.result(timeout=90)

    word_list = []

    for result in result.results:
        alternative = result.alternatives[0]
        for word_info in alternative.words:
            word = word_info.word
            start_time = word_info.start_time
            if not (word in stops):
                word_list.append({
                    str(word): start_time.total_seconds()
                })
    return word_list
