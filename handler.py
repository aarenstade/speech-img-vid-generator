# take in audio file
# convert audio file to text
# split text into list of words, w timecode
# get timecode of each word

# get total time of audio file
# with ffmpeg, write image for every frame it exists
# do this for all frames until end


# Python program to translate
# speech to text and text to speech
#   Transcript: hello my name is
# Confidence: 0.9754610061645508
# Word: hello, start_time: 0.5, end_time: 1.0
# Word: my, start_time: 1.0, end_time: 1.3
# Word: name, start_time: 1.3, end_time: 1.4
# Word: is, start_time: 1.4, end_time: 1.7

from process_speech import ProcessSpeech
from build_video import BuildVideo
from pydub import AudioSegment
import os


# TODO: prepare more types of audio

def prepare_audio(audio_path):
    new_path = audio_path + '_MONO.wav'
    sound = AudioSegment.from_wav(audio_path + '.wav')
    sound = sound.set_channels(1)
    sound.export(new_path, format="wav")
    return new_path


def remove_frames(path):
    if(os.path.exists(path)):
        os.remove(path)


def Handler():
    title = input("Video Title: ")
    src_audio = input("Audio filename: ")
    audio_path = prepare_audio(src_audio)
    PATH = "./" + title
    word_list = ProcessSpeech(audio_path)
    BuildVideo(PATH, title, audio_path, word_list)
    remove_frames(PATH)


Handler()
