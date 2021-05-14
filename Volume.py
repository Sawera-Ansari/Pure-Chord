from tkinter import *
from tkinter import ttk
from pygame import mixer

class Volume(Frame):

    def __init__(self, rightframe):

        super().__init__(rightframe)

        self.muted = FALSE

        self.mutePhoto = PhotoImage(file='images\mute.png')
        self.volumePhoto = PhotoImage(file='images/volume.png')
        self.volumeBtn = ttk.Button(self, image=self.volumePhoto, command=self.mute_music)
        self.volumeBtn.grid(row=0, column=1)

        self.scale = ttk.Scale(self, from_=0, to=100, orient=HORIZONTAL, command=self.set_vol)
        self.scale.set(30)  # implement the default value of scale when music player starts
        mixer.music.set_volume(0.3)
        self.scale.grid(row=0, column=2, pady=15, padx=30)

    def set_vol(self, val):
        volume = float(val) / 100
        mixer.music.set_volume(volume)
        if volume!=0:
            self.volume=volume
            self.val=val
            self.volumeBtn.configure(image=self.volumePhoto)
        else:
            self.volumeBtn.configure(image=self.mutePhoto)

        # set_volume of mixer takes value only from 0 to 1. Example - 0, 0.1,0.55,0.54.0.99,1

    def mute_music(self):
        if self.muted:  # Unmute the music
            mixer.music.set_volume(self.volume)
            self.volumeBtn.configure(image=self.volumePhoto)
            self.scale.set(self.val)
            self.muted = FALSE
        else:  # mute the music
            mixer.music.set_volume(0)
            self.volumeBtn.configure(image=self.mutePhoto)
            self.scale.set(0)
            self.muted = TRUE
