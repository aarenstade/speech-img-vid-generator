from process.audio.process_audio import ProcessAudio
from process.audio.process_speech import ProcessSpeech
from process.video.build_video import BuildVideo
from utils.log import Log_Word_List, Log_Final
import time
import os
import shutil


# gen_version
# 0 --> default accurate images
# 1 --> random, not accurate images

def create_dir(path):
    if not (os.path.exists(path)):
        os.makedirs(path)


def remove_dir(path):
    print("DELETING DIR", path)
    if(os.path.exists(path)):
        shutil.rmtree(path)


def Process_Handler(logger, creds_path, bucket_name, video_title, audio_path, gen_version):
    start = time.time()
    PATH = "./" + 'OUTPUT/' + video_title
    create_dir(PATH)
    audio_path = ProcessAudio(logger, video_title, PATH, audio_path)
    word_list = ProcessSpeech(logger, audio_path, video_title)
    Log_Word_List(logger, word_list)
    vid_path = BuildVideo(logger, PATH, video_title, audio_path, word_list)
    remove_dir(PATH + '/frames')
    remove_dir(PATH + '/src')
    end = time.time()
    Log_Final(logger, video_title, (end - start), vid_path)
