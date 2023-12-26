import os
import pygame
import io
from mutagen.id3 import ID3
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk

class MP3Player:
    def __init__(self, master):
        self.master = master
        self.master.title("MP3 Player")
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
        
        self.stop_button = Button(self.button_frame1, text="Stop", command=self.stop, bg='beige')
        self.stop_button.pack(side=LEFT, padx=0, fill=BOTH, expand=True)

        self.skip_button = Button(self.button_frame1, text="Skip", command=self.skip, bg='beige')
        self.skip_button.pack(side=LEFT, padx=0, fill=BOTH, expand=True)

        self.button_frame2 = Frame(self.master, bg='black')
        self.button_frame2.pack(pady=0, fill=BOTH, expand=True)
        
        self.add_button = Button(self.button_frame2, text="Add Song", command=self.add_song, bg='beige')
        self.add_button.pack(side=LEFT, padx=0, fill=BOTH, expand=True)

        self.load_button = Button(self.button_frame2, text="Load Playlist", command=self.load_playlist, bg='beige')
        self.load_button.pack(side=LEFT, padx=0, fill=BOTH, expand=True)

        self.playlist = Listbox(self.master, selectmode=MULTIPLE, bg='beige', fg='black')  # ファイル名表示部分の背景と文字色を変更
        self.playlist.pack(pady=20, padx=0, fill=BOTH, expand=True)

        self.album_art_label = Label(self.master, bg='black')
        self.album_art_label.pack(pady=0)

        self.song_list = []

    def load_playlist(self):
        directory = filedialog.askdirectory()
        if directory:
            os.chdir(directory)
            self.song_list = [file for file in os.listdir() if file.endswith(".mp3")]
            self.playlist.delete(0, END)
            for song in self.song_list:
                self.playlist.insert(END, song)

    def add_song(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("MP3 files", "*.mp3")])
        if file_paths:
            new_songs = [os.path.basename(file) for file in file_paths]
            self.song_list.extend(new_songs)
            for song in new_songs:
                self.playlist.insert(END, song)

    def play(self):
        selected_index = self.playlist.curselection()
        if selected_index:
            selected_song = self.song_list[selected_index[0]]
            pygame.mixer.init()
            pygame.mixer.music.load(selected_song)
            pygame.mixer.music.play()
            self.display_album_art(selected_song)

    def stop(self):
        pygame.mixer.music.stop()
        self.album_art_label.config(image='')

    def skip(self):
        pygame.mixer.music.stop()
        next_index = (self.playlist.curselection()[-1] + 1) % len(self.song_list)
        next_song = self.song_list[next_index]
        self.playlist.selection_clear(0, END)
        self.playlist.selection_set(next_index)
        self.playlist.activate(next_index)
        pygame.mixer.music.load(next_song)
        pygame.mixer.music.play()
        self.display_album_art(next_song)

    def back(self):
        pygame.mixer.music.stop()
        prev_index = (self.playlist.curselection()[0] - 1) % len(self.song_list)
        prev_song = self.song_list[prev_index]
        self.playlist.selection_clear(0, END)
        self.playlist.selection_set(prev_index)
        self.playlist.activate(prev_index)
        pygame.mixer.music.load(prev_song)
        pygame.mixer.music.play()
        self.display_album_art(prev_song)

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

if __name__ == "__main__":
    root = Tk()
    mp3_player = MP3Player(root)
    root.mainloop()
