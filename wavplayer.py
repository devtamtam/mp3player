import os
import pygame
import io
from mutagen.id3 import ID3
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk

class wavPlayer:
    def __init__(self, master):
        self.master = master
        self.master.title("wav Player")
        self.master.geometry("300x680")

        # 背景を黒に設定
        self.master.configure(bg='black')

        pygame.init()

        self.button_frame1 = Frame(self.master, bg='black')
        self.button_frame1.pack(pady=0, fill=BOTH, expand=True)

        # ボタンをベージュ色に設定
        self.back_button = Button(self.button_frame1, text="Back", command=self.back, bg='beige')
        self.back_button.pack(side=LEFT, padx=0, fill=BOTH, expand=True)

        self.play_button = Button(self.button_frame1, text="Play", command=self.play, bg='darkred')
        self.play_button.pack(side=LEFT, padx=0, fill=BOTH, expand=True)

        self.skip_button = Button(self.button_frame1, text="Skip", command=self.skip, bg='yellow')
        self.skip_button.pack(side=LEFT, padx=0, fill=BOTH, expand=True)

        self.button_frame2 = Frame(self.master, bg='black')
        self.button_frame2.pack(pady=0, fill=BOTH, expand=True)

        self.stop_button = Button(self.button_frame2, text="Stop", command=self.stop, bg='beige')
        self.stop_button.pack(side=LEFT, padx=0, fill=BOTH, expand=True)

        self.button_frame3 = Frame(self.master, bg='black')
        self.button_frame3.pack(pady=0, fill=BOTH, expand=True)

        self.add_button = Button(self.button_frame3, text="Add Song", command=self.add_song, bg='beige')
        self.add_button.pack(side=LEFT, padx=0, fill=BOTH, expand=True)

        self.load_button = Button(self.button_frame3, text="Load Playlist", command=self.load_playlist, bg='blue')
        self.load_button.pack(side=LEFT, padx=0, fill=BOTH, expand=True)

        self.playlist = Listbox(self.master, selectmode=MULTIPLE, bg='beige', fg='black')  # ファイル名表示部分の背景と文字色を変更
        self.playlist.pack(pady=20, padx=0, fill=BOTH, expand=True)

        self.album_art_label = Label(self.master, bg='black')
        self.album_art_label.pack(pady=0)

        self.song_list = []
        self.current_song_index = 0

        # 自動再生用の変数
        self.auto_play_enabled = True

    def load_playlist(self):
        directory = filedialog.askdirectory()
        if directory:
            os.chdir(directory)
            self.song_list = [file for file in os.listdir() if file.endswith(".wav")]
            self.playlist.delete(0, END)
            for song in self.song_list:
                self.playlist.insert(END, song)

    def add_song(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("wav files", "*.wav")])
        if file_paths:
            new_songs = [os.path.basename(file) for file in file_paths]
            self.song_list.extend(new_songs)
            for song in new_songs:
                self.playlist.insert(END, song)

    def play(self):
        if not pygame.mixer.music.get_busy():
            self.auto_play_enabled = True
            self.play_current_song()

    def stop(self):
        pygame.mixer.music.stop()
        self.album_art_label.config(image='')
        self.auto_play_enabled = False

    def skip(self):
        self.stop()
        self.current_song_index = (self.current_song_index + 1) % len(self.song_list)
        self.play_current_song()

    def back(self):
        self.stop()
        self.current_song_index = (self.current_song_index - 1) % len(self.song_list)
        self.play_current_song()

    def display_album_art(self, song):
        try:
            audio = ID3(song)
            artwork_data = audio.getall('APIC')[0].data
            image = Image.open(io.BytesIO(artwork_data))
            image.thumbnail((300, 300))
            image = ImageTk.PhotoImage(image)
            self.album_art_label.config(image=image)
            self.album_art_label.image = image
        except (KeyError, IndexError):
            # No album artwork found
            self.album_art_label.config(image='')

    def check_song_end(self):
        if not pygame.mixer.music.get_busy() and self.auto_play_enabled:
            self.current_song_index = (self.current_song_index + 1) % len(self.song_list)
            self.play_current_song()

    def play_current_song(self):
        selected_song = self.song_list[self.current_song_index]
        pygame.mixer.init()
        pygame.mixer.music.load(selected_song)
        pygame.mixer.music.play()
        self.display_album_art(selected_song)

        if self.auto_play_enabled:
            self.master.after(100, self.check_song_end)

if __name__ == "__main__":
    root = Tk()
    wav_player = wavPlayer(root)
    root.mainloop()
