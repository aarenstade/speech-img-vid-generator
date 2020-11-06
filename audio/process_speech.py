import io
import os
import time
from google.cloud import speech
from google.cloud import storage
from nltk.corpus import stopwords
from utils.log import Log_Transcript
from pydub import AudioSegment


# Settings for image arrangement & video
# Attach main vocal audio section, or record
# Optional music

# List of text fields and image attachments
# So we can use select images for select words


bucket_name = "comdev-30131.appspot.com"

stops = stopwords.words('english')
more_stops = [
    'like',
    'past',
    'the',
    'The',
    'definitely',
    'many',
    'parts',
    'completely',
    'entirely',
    'either',
    'got',
    'would',
    'could',
    'probably',
    'may',
    'back',
    'I',
    "I'll"
    "I'm",
    'ton',
    'especially',
    'maybe',
    'want',
    'wanted',
]


def return_result(result):
    word_list = []
    for result in result.results:
        alternative = result.alternatives[0]
        transcript = alternative.transcript
        Log_Transcript(transcript, './')
        for word_info in alternative.words:
            word = word_info.word
            start_time = word_info.start_time
            if not (word in stops):
                if not (word in more_stops):
                    word_list.append({
                        str(word): start_time.total_seconds()
                    })
    return word_list


def ProcessShortSpeech(filename):
    print("SPEECH TO TEXT (short)", filename)
    start = time.time()
    client = speech.SpeechClient()
    with io.open(filename, mode='rb') as audio:
        # get sample rate and assign sample rate
        content = audio.read()
        audio = speech.RecognitionAudio(content=content)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=11025,
        language_code="en-US",
        enable_word_time_offsets=True
    )

    request = client.long_running_recognize(config=config, audio=audio)
    print('AWAITING API RESPONSE')
    result = request.result(timeout=90)
    end = time.time()
    print("Speech to text took", round((end - start)), "seconds")
    word_list = return_result(result)
    return word_list


def upload_audio_file(filename, title):
    client = storage.Client.from_service_account_json(
        json_credentials_path='/Users/aarenstade/google-credentials.json')
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(filename)
    print('Uploading Audio', filename)
    start = time.time()
    blob.upload_from_filename(filename)
    end = time.time()
    print('Uploaded in', round((end - start)), "seconds")
    final_link = 'gs://' + bucket_name + "/" + filename
    return final_link


def ProcessLongRunningSpeech(filename, title):
    print('SPEECH TO TEXT (long runnning)', filename)
    upload_file_uri = upload_audio_file(filename, title)
    start = time.time()
    client = speech.SpeechClient()
    audio = speech.RecognitionAudio(uri=upload_file_uri)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=48000,
        language_code="en-US",
        enable_word_time_offsets=True
    )
    operation = client.long_running_recognize(
        request={"config": config, "audio": audio}
    )
    operation = client.long_running_recognize(config=config, audio=audio)
    print('AWAITING LONG RUNNING API RESPONSE')
    result = operation.result(timeout=90)
    end = time.time()
    print("Speech to text took", round((end - start)), "seconds")
    word_list = return_result(result)
    return word_list


def ProcessSpeech(filename, title):
    sound = AudioSegment.from_wav(filename)
    duration = sound.duration_seconds
    if(duration > 60):
        word_list = ProcessLongRunningSpeech(filename, title)
        return word_list
    else:
        word_list = ProcessShortSpeech(filename)
        return word_list
