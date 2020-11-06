from pydub import AudioSegment
import os


def open_file(audio_path, file_type):
    if (file_type == "wav"):
        sound = AudioSegment.from_wav(audio_path)
        return sound
    elif (file_type == "mp3"):
        sound = AudioSegment.from_mp3(audio_path)
        return sound
    elif (file_type == "ogg"):
        sound = AudioSegment.from_mp3(audio_path)
        return sound
    elif (file_type == "aac"):
        sound = AudioSegment.from_mp3(audio_path)
        return sound
    elif (file_type == "flv"):
        sound = AudioSegment.from_mp3(audio_path)
        return sound
    elif (file_type == "wma"):
        sound = AudioSegment.from_mp3(audio_path)
        return sound


def convert_to_wav(audio_path, file_type):
    sound = open_file(audio_path, file_type)
    sound = sound.set_channels(1)
    dot_index = str(audio_path).index('.')
    new_path = audio_path[:dot_index] + '_MONO.wav'
    sound.export(new_path, format="wav")
    print("Audio Size: ", str(round(os.path.getsize(new_path) / 1048576)) + " MB")
    return new_path


def ProcessAudio(audio_path):
    print("AUDIO PROCESSING", audio_path)
    dot_index = str(audio_path).index('.')
    file_type = str(audio_path)[dot_index+1:]
    new_audio = convert_to_wav(audio_path, file_type)
    return new_audio
