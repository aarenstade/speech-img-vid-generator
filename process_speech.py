import io
import os
from google.cloud import speech

client = speech.SpeechClient()


def ProcessSpeech(filename):
    print("Processing Speech")
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
    print('Awaiting API response')
    result = request.result(timeout=90)

    word_list = []

    # TODO: create return data format and return
    for result in result.results:
        alternative = result.alternatives[0]
        print("Transcript: {}".format(alternative.transcript))
        for word_info in alternative.words:
            word = word_info.word
            start_time = word_info.start_time
            word_list.append({
                str(word): start_time.total_seconds()
            })
    return word_list
