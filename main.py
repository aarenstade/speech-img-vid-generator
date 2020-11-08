import tkinter as tk
import threading
import logging
from logging_gui import ConsoleUi
from tkinter.scrolledtext import ScrolledText
import queue

logger = logging.getLogger(__name__)


class RootWindow:
    def __init__(self, root):
        self.root = root
        self.root.title('ImgVidGen')
        self.root.geometry('800x700')

        main_title = tk.Label(self.root, text="Image Video Generator", font=(
            "Helvetica", 30)).pack(pady=10)

        # SETUP SECTION
        setup_title = tk.Label(self.root, text='Setup',
                               font=("Helvetica", 22)).pack()
        self.creds_path = tk.StringVar()
        creds_path_label = tk.Label(
            self.root, textvariable=self.creds_path).pack()
        creds_button = tk.Button(
            self.root, text="Select Google Credentials JSON", command=self.select_creds).pack()

        bucket_label = tk.Label(
            self.root, text='Google Storage Bucket URI').pack()
        bucket_entry = tk.Entry(self.root, width=20).pack(pady=5)

        # VIDEO DETAILS SECTION
        video_details_title = tk.Label(
            self.root, text='Video Details', font=("Helvetica", 22)).pack(pady=5)

        # video title
        video_title_label = tk.Label(self.root, text='Video Title:').pack()
        self.video_title_entry = tk.Entry(self.root, width=20).pack(pady=5)

        # audio file
        self.audio_path = tk.StringVar()
        audio_path_label = tk.Label(
            self.root, textvariable=self.audio_path).pack()
        audio_button = tk.Button(
            self.root, text="Choose Audio", command=self.select_audio).pack()

        # choose gen_version, return 0 or 1
        # choose output path, and use that as root path

        # run button, do check

        # CONSOLE
        console_frame = tk.Frame(self.root)
        console_frame.pack()
        self.console = ConsoleUi(logger, console_frame)

    def start(self):
        self.root.mainloop()

    def select_creds(self):
        filename = tk.filedialog.askopenfilename()
        self.creds_path.set(filename)

    def select_audio(self):
        filename = tk.filedialog.askopenfilename()
        self.audio_path.set(filename)


def main():
    logging.basicConfig(level=logging.DEBUG)
    root = tk.Tk()
    window = RootWindow(root)
    window.start()


if __name__ == '__main__':
    main()
