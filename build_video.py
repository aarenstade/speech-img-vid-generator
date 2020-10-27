import subprocess
import os
import wave
from PIL import Image
from make_frame import CreateFrame


def get_total_time(audio_file):
    f = wave.open(audio_file, 'rb')
    samples = f.getnframes()
    samplerate = f.getframerate()
    total_sec = samples / samplerate
    return total_sec


def create_frames_dir(title, PATH):
    path = PATH + '/' + "frames"
    if not (os.path.exists(path)):
        os.makedirs(path)
    return path


def create_frames(word_list, FRAMERATE, TOTAL_SEC, FRAMES_PATH):
    print("writing frames before first word")
    (first_word, first_time), = word_list[0].items()
    first_word_frame = round(first_time * FRAMERATE)
    for i in range(first_word_frame):
        img = Image.new('RGB', (1280, 720))
        img.save(FRAMES_PATH + '/' + str(i).zfill(3) + '.jpg')
    print("writing frames for each word")
    for i in range(len(word_list)):
        (word, time), = word_list[i].items()
        print(word, time)
        try:
            (nextWord, nextTime), = word_list[i+1].items()
        except:
            nextTime = TOTAL_SEC
            pass
        frame = CreateFrame(word)  # create collage
        start_frame = round(time * FRAMERATE)
        end_frame = round(nextTime * FRAMERATE)
        total_frames = end_frame - start_frame
        if(frame != None):
            for i in range(total_frames):
                filename = str(start_frame + i).zfill(3) + '.jpg'
                frame.save(FRAMES_PATH + '/' + filename)
        else:
            for i in range(total_frames):
                filename = str(start_frame + i).zfill(3) + '.jpg'
                frame = Image.new('RGB', (1280, 720))
                frame.save(FRAMES_PATH + '/' + filename)


def BuildVideo(PATH, title, audio_path, word_list):
    FRAMERATE = 12
    TOTAL_SEC = get_total_time(audio_path)
    FRAMES_PATH = create_frames_dir(title, PATH)
    create_frames(word_list, FRAMERATE, TOTAL_SEC, FRAMES_PATH)
    OUTPUT_FILE = title + '.mp4'
    command = "ffmpeg -framerate " + str(FRAMERATE) + " -i " + FRAMES_PATH + \
        "/%03d.jpg -i " + audio_path + " -strict -2 " + OUTPUT_FILE
    print('generating video')
    subprocess.call(command, shell=True)
    print('video created')
