from audio.process_audio import ProcessAudio
from audio.process_speech import ProcessSpeech
from audio.music import RandomMusic, CombineAudio
from video.build_video import BuildVideo
import utils.log as log
import time
import os
import shutil


# TODO: Do some more tests, and think of how this could be improved...


# Potential features:
# Intro text
# Background music
# Input description and automatically upload to YouTube


# Somehow specify key words even further beyond removing stop words


def create_dir(path):
    if not (os.path.exists(path)):
        os.makedirs(path)


def remove_dir(path):
    print("DELETING DIR", path)
    if(os.path.exists(path)):
        shutil.rmtree(path)


def Handler():
    title = input('Video Title: ')
    audio = input('Audio File: ')
    start = time.time()
    PATH = "./" + 'OUTPUT/' + title
    create_dir(PATH)
    audio_path = ProcessAudio(audio)
    word_list = ProcessSpeech(audio_path, title)
    log.Log_Word_List(word_list, PATH)
    vid_path = BuildVideo(PATH, title, audio_path, word_list)
    remove_dir(PATH + '/frames')
    remove_dir(PATH + '/src')
    end = time.time()
    log.Log_Final(title, (end - start), vid_path)


Handler()
