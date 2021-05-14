import tkinter.messagebox
from ttkthemes.themed_tk import ThemedTk
from tkinter import filedialog
import tkinter.messagebox
from tkinter import simpledialog
import tkinter.messagebox
from tkinter import *
import time
import threading
from tkinter import ttk
from mutagen.mp3 import MP3
import os
from pygame import mixer
from Volume import Volume


class Music(Frame):

    def __init__(self, rightframe, statusbar, leftframe):

        # Initialising all the necassary variables and objects...
        self.n = 0
        self.play_it = -1
        self.leftframe = leftframe
        self.statusbar = statusbar
        self.playlistbox = self.leftframe.playlistbox
        self.playlist = self.leftframe.playlist
        self.breakvariable = False

        super().__init__(rightframe)

        # Creating all the labels.
        self.lengthlabel = ttk.Label(self, text='Total Length : --:--')
        self.lengthlabel.grid(row=0, column=1, padx=10, pady=10)

        self.currenttimelabel = ttk.Label(self, text='Current Time : --:--', relief=GROOVE)
        self.currenttimelabel.grid(row=1, column=1, padx=10, pady=10)

        # Loading all the photos that will be used over the buttons (play/pause, forward, back)...
        self.playPhoto = PhotoImage(file='images/play.png')
        self.pausePhoto = PhotoImage(file='images/pause.png')
        self.forwardPhoto = PhotoImage(file='images/forward.png')
        self.backPhoto = PhotoImage(file='images/back.png')

        # Creating Buttons; Play button, Forward button, Back button.
        self.forwardBtn = ttk.Button(self, image=self.forwardPhoto, command=self.forward)
        self.backBtn = ttk.Button(self, image=self.backPhoto, command=self.back)
        self.playBtn = ttk.Button(self, image=self.playPhoto, command=self.start_stop)
        self.playBtn.grid(row=2, column=1)
        self.forwardBtn.grid(row=2, column=2)
        self.backBtn.grid(row=2, column=0)

        # Associating song 'play' action with mice's double click...
        self.playlistbox.bind('<Double-1>', lambda x:self.playOnClick())

    def back(self):
        try:
            self.updatePlaylist()
            self.play_it = int(self.playlistbox.curselection()[0])   # listbox.curselection() -> returns: tuple containing index of the line which is curently highlighted.
            self.play_it -= 1
            if self.play_it == -1:    # when the playlist index gets out of range after the first item in the list, self.play_it is reset to the last item of playlist.
                self.play_it = len(self.playlist) - 1
            MainGUI.Index = self.play_it
            MainGUI.SONG = self.playlist[self.play_it]
            mixer.music.stop()          # the current song is stopped first...
            self.n = 1
            time.sleep(1)
            mixer.music.load(MainGUI.SONG)
            mixer.music.play(0)
            self.playBtn.configure(image=self.pausePhoto)
            self.statusbar['text'] = "Music Playing" + ' - ' + os.path.basename(self.playlist[self.play_it])
            self.show_details(self.playlist[self.play_it])
            # set the cursor highlight on the new song..
            self.playlistbox.selection_clear(0, END)
            self.playlistbox.selection_set(MainGUI.Index)
        except IndexError:
            pass
        except AttributeError:
            pass

    def forward(self):
        try:
            self.updatePlaylist()
            self.play_it = int(self.playlistbox.curselection()[0])
            self.play_it += 1           # setting the index of the next song in queue...
            if self.play_it == len(self.playlist):      # when list gets out of range, the index variable is set to 0.
                self.play_it = 0
            MainGUI.Index = self.play_it
            MainGUI.SONG = self.playlist[self.play_it]
            mixer.music.stop()
            self.n = 1
            time.sleep(1)
            mixer.music.load(MainGUI.SONG)
            mixer.music.play(0)
            self.playBtn.configure(image=self.pausePhoto)
            self.statusbar['text'] = "Music Playing" + ' - ' + os.path.basename(self.playlist[self.play_it])
            self.show_details(self.playlist[self.play_it])
            # reset the cursor selection...
            self.playlistbox.selection_clear(0, END)
            self.playlistbox.selection_set(MainGUI.Index)
        except IndexError:
            pass
        except AttributeError:
            pass

    def updatePlaylist(self):
        '''This method updates the playlist and playlistbox being used in this class by re-assigning the
        Playlist class's playlist and playlistbox (being accessed by the object self.c which is an instance of
        Playlist) to variables self.playlist and self.playlistbox.'''
        self.playlist = self.leftframe.playlist
        self.playlistbox = self.leftframe.playlistbox

    def playOnClick(self):
        try:
            self.updatePlaylist()
            self.cursorselection = self.playlistbox.curselection()
            self.play_it = int(self.cursorselection[0])
            MainGUI.SONG = self.playlist[self.play_it]
            MainGUI.Index = self.play_it
            mixer.music.stop()
            self.n = 1
            time.sleep(1)
            mixer.music.load(self.playlist[self.play_it])
            mixer.music.play(0)
            self.playBtn.configure(image=self.pausePhoto)
            self.show_details(self.playlist[self.play_it])
        except:
            pass

    def start_stop(self):
        '''This method allows user to perform play, pause and unpause actions through a single button.
        self.n = 0; state of music when it enters this method.
        self.n = 1; music plays from the beginning.
        self.n = 2; music pauses (self.n can be any even number value)
        self.n = 3; music unpauses (self.n can be any odd number value)'''
        try:
            self.updatePlaylist()
            if self.breakvariable == True:
                self.n = 0
            self.n += 1
            self.cursorselection = self.playlistbox.curselection()
            self.play_it = int(self.cursorselection[0])
            # if the highlighted song is not the song being currently played then set self.n = 1 so that the current song be stopped and highlighted song can be played...
            if MainGUI.SONG!=self.playlist[self.play_it] and MainGUI.SONG != '':
                mixer.music.stop()
                self.n = 1
                time.sleep(1)
            if self.n == 1:
                mixer.music.load(self.playlist[self.play_it])
                mixer.music.play(0)
                self.playBtn.configure(image=self.pausePhoto)
                self.show_details(self.playlist[self.play_it])
                MainGUI.SONG = self.playlist[self.play_it]
                MainGUI.Index = self.play_it
            elif (self.n % 2) == 0:
                mixer.music.pause()
                self.playBtn.configure(image=self.playPhoto)
                self.statusbar['text'] = 'Music Paused - ' + os.path.basename(self.playlist[self.play_it])
            elif (self.n % 2) != 0:
                mixer.music.unpause()
                self.playBtn.configure(image=self.pausePhoto)
                self.statusbar['text'] = "Music Playing" + ' - ' + os.path.basename(self.playlist[self.play_it])
        except:             # when self.play_it has no value, tkinter will show an error message to the user...
            tkinter.messagebox.showerror('File not found', 'Pure Chord could not find the file. Please check again.')
            self.n = 0

    def show_details(self,play_song):
        '''This method collects and shows the time duration of the song.'''

        # self.file_data contains the allowed file extension (either .mp3 or .wav)
        self.file_data = os.path.splitext(play_song)
        if self.file_data[1] == '.mp3':  # file is a .mp3 file so time  metadata is extracted by using mutagen module
            self.audio = MP3(play_song)
            self.total_length = self.audio.info.length
        else:   # for .wav files Sound class of mixer is used.
            a = mixer.Sound(play_song)
            self.total_length = a.get_length()

        # converting time to mins and secs and updating the text of self.length label after applying some formatting...
        # div - total_length/60, mod - total_length % 60
        mins, secs = divmod(self.total_length, 60)
        mins = round(mins)
        secs = round(secs)
        self.timeformat2 = '{:02d}:{:02d}'.format(mins, secs)
        self.lengthlabel['text'] = "Total Length" + ' - ' + self.timeformat2

        # creating a new thread for start_count method it does not affect the main thread
        self.t1 = threading.Thread(target=self.start_count)
        self.t1.start()


    def start_count(self):
        # mixer.music.get_busy(): - Returns FALSE when we press the stop button (music stop playing) or music finishes.
        # Continue - Ignores all of the statements below it. We check if music is paused or not.
        self.current_time = 0
        self.breakvariable = False
        while self.current_time <= self.total_length and mixer.music.get_busy():
            if (self.n%2) == 0 or self.n == 0:
                continue
            else:
                # self.current_time -> starts from 0 untill the music finishes and mixer.get_busy() gives False.
                if mixer.music.get_busy():
                    self.statusbar['text'] = "Music Playing" + ' - ' + os.path.basename(MainGUI.SONG)
                    mins, secs = divmod(self.current_time, 60)
                    mins = round(mins)
                    secs = round(secs)
                    self.timeformat = '{:02d}:{:02d}'.format(mins, secs)
                    self.currenttimelabel['text'] = "Current Time" + ' - ' + self.timeformat
                    time.sleep(1)
                    self.current_time += 1
                else:
                    time.sleep(1)
                    self.breakvariable = True   # self.breakvariable when True sets the music's state, self.n, to 1 so that it can be restarted if play/pause button is pressed.
                    break


class Playlist(Frame):

    def __init__(self, window):

        super().__init__(window)

        self.playlist = []

        # inside_frame contains playlistbox and two scrollbars; horizontal and vertical.
        # Buttons; Add, Delete, Save; are in the outside frame ie Playlist Class frame.

        inside_frame=Frame(self)
        inside_frame.pack(pady=3)

        self.scrollbar1=Scrollbar(inside_frame)
        self.scrollbar1.pack(side=RIGHT, fill=Y)
        self.scrollbar2 = Scrollbar(inside_frame, orient=HORIZONTAL)
        self.scrollbar2.pack(side=BOTTOM, fill=X)

        self.playlistbox = Listbox(inside_frame, selectmode=EXTENDED, width=45, height=15)
        self.playlistbox.pack()
        self.playlistbox.config(yscrollcommand=self.scrollbar1.set)
        self.scrollbar1.config(command=self.playlistbox.yview)
        self.playlistbox.config(xscrollcommand=self.scrollbar2.set)
        self.scrollbar2.config(command=self.playlistbox.xview)

        self.create_playlist()

    def create_playlist(self):
        '''This method creates buttons; Add, Delete, Save in the Playlist Class frame'''

        addBtn = ttk.Button(self, text="+ Add", command=self.browse_file)
        addBtn.pack(side=LEFT)

        delBtn = ttk.Button(self, text="- Delete", command=self.del_songs)
        delBtn.pack(side=LEFT)

        savBtn = ttk.Button(self, text="Save", command=self.save_playlist)
        savBtn.pack(side=LEFT)

    def add_to_playlist(self, filename):
        '''This method takes file path (filename) as parameter and adds it to the playlist of user and also shows
        the name of the file in the playlistbox'''
        try:
            # os.path.basename -> takes the absolute path of a file and returns the name of the file...
            filename_path = filename
            filename = os.path.basename(filename)
            index = 0
            self.playlistbox.insert(index, filename)        # always inserts the new .mp3 file on 0th index of playlistbox so that it appears on top of all other files in the playlistbox
            self.playlist.insert(index, filename_path)      # always inserts the new .mp3 file on 0th index of playlist.
            index += 1
            mixer.music.queue(filename_path)
            # reset the MainGUI.Index as indices change after new song files are added in the playlisbox.
            MainGUI.Index = int(self.playlistbox.curselection()[0])
        except:
            pass

    def upload_playlist(self, pl_file_name):
        '''A .txt files saves the paths of the songs inside a list.
        This method takes the name of that .txt file as parameter, reads and creates a temporary list
        (new_playlist) of all the songs written in the file and calls add_to_playlist() method for each
        item in the list'''

        choice=tkinter.messagebox.askquestion('Where to place?', f'Do you want to open {pl_file_name} as new playlist?')
        if choice=='yes':       # yes -> all the files currently available in the playlistbox are deleted and new playlist is uploaded.
            self.playlist=[]
            self.playlistbox.delete(0,END)
            mixer.music.stop()
        f = open(pl_file_name, 'r')
        new_playlist = eval(f.read())
        f.close()
        for song in new_playlist:
            self.add_to_playlist(song)
            mixer.music.queue(song)

    def browse_file(self):
        '''This method allows user to open mp3/wav file from their computers'''
        filename_path = filedialog.askopenfilename()
        if filename_path != '':
            self.add_to_playlist(filename_path)
            mixer.music.queue(filename_path)

    def save_playlist(self):
        '''This method creates a new text file and writes self.playlist in it
        self.playlist is a list that contains file paths of all the songs'''

        if self.playlist != []:
            # simpledialog.askstring -> asks for the name of the playlist & saves it in pl_fle_name
            pl_file_name = simpledialog.askstring(title="Save Playlist",
                                                  prompt="Playlist name:")
            f = open(pl_file_name + '.txt', 'w')
            f.write(str(self.playlist))
            f.close()
        else:
            tkinter.messagebox.showerror('Playlist Not Found', 'First upload some mp3 files and then make a  playlist.')

    def del_playlist(self, pl_file_name):
        '''This method takes name (along with the extension) of the text file in which the respective playlist
        was saved and deletes it from the system.'''
        os.remove(pl_file_name)

    def del_songs(self):
        '''This method deletes all the songs highlighted by the cursor in one go.'''
        try:
            # selected_songs is a tuple containing all the indices of highlighted songs
            # selected_song is the item (song) in the self.playlist against the index i
            selected_songs = self.playlistbox.curselection()
            count = 0
            for i in selected_songs:
                selected_song = self.playlist[i]

                # we compare selected_song with the MainGUI.SONG and MainGUI.Index with i to check if the highlighted song is same
                # as the current song. If True, the music stops playing after the current song is deleted.
                if MainGUI.SONG == selected_song and MainGUI.Index == i:
                    mixer.music.stop()

                # count increases if the song getting deleted lies above the current song in the playlistbox
                # the first song in the playlistbox has index 0 and index increases as we go down the list box
                if i < MainGUI.Index:
                    count += 1

                self.playlistbox.delete(i)
                self.playlistbox.insert(i,'')
                self.playlist.pop(i)
                self.playlist.insert(i, '')
        except IndexError:
            tkinter.messagebox.showerror('No File Found', 'no file selected.')
        finally:
            PLaylist = []
            for item in self.playlist:
                if item != '':
                    PLaylist.append(item)
            self.playlist = PLaylist
            self.playlistbox.delete(0,END)
            for items in self.playlist[::-1]:
                index = 0
                self.playlistbox.insert(index, os.path.basename(items))
                index += 1

        # Cursor selection is set back to the current song's index ie MainGUI.Index
        if count > 0:
            # count has the value equal to the number of songs that lie above current song in the list and have got deleted now.
            # Thus it is subtracted from the MainGUI.Index to shift the cursor highlight count places upwards.
            MainGUI.Index -= count
            self.playlistbox.selection_set(MainGUI.Index)
        else:
            self.playlistbox.selection_set(MainGUI.Index)

class MainGUI(ThemedTk):

    def __init__(self):
        super().__init__()

        MainGUI.SONG = ''       # class var; stores name of current song.
        MainGUI.Index = -1      # class var; stores index of current song.

        self.minsize(863, 404)
        self.maxsize(863, 404)

        self.setPosition()

        mixer.init()

        leftframe = Playlist(self)      # instantiating Playlist class's object

        #settng the theme, title and icon of the tkinter window.
        self.set_theme('radiance')
        self.title("Pure Chord")
        self.iconbitmap(r'images/pure_chord.ico')

        statusbar = self.create_statusbar()

        self.create_menubar(leftframe.browse_file, leftframe.upload_playlist, leftframe.del_playlist)

        self.rightframe = Frame(self)       # self.rightframe contains Volume and Music class's frames.

        self.middleframe = Music(self.rightframe, statusbar, leftframe)

        leftframe.pack(side=LEFT, padx=30, pady=30)

        self.rightframe.pack(pady=30)

        self.middleframe.pack(pady=30, padx=30)

        self.bottomframe = Volume(self.rightframe)
        self.bottomframe.pack(pady=20)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.mainloop()

    def setPosition(self):
        '''Fixes the position where the window opens on the screen.'''

        w = 863  # width for the Tk root
        h = 404  # height for the Tk root

        # get screen width and height
        ws = self.winfo_screenwidth()  # width of the screen
        hs = self.winfo_screenheight()  # height of the screen

        # calculate x and y coordinates for the Tk root window
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2) - 100

        # set the dimensions of the screen
        # and where it is placed
        self.geometry('%dx%d+%d+%d' % (w, h, x, y))

    def create_statusbar(self):
        statusbar = ttk.Label(self, text="Welcome to Pure Chord", relief=SUNKEN, anchor=W, font='Times 10 italic')
        statusbar.pack(side=BOTTOM, fill=X)
        return statusbar

    def on_closing(self):
        '''This method is executed when user exits the application.
        It stops the music when the application is closed.'''
        mixer.music.stop()
        self.destroy()

    def create_menubar(self, browse_file, upload_playlist, del_playlist):
        '''This method creates a menubar in the main window.'''

        def about_us():
            tkinter.messagebox.showinfo('About Pure Chord',
                                        'This is a music player build using Python modules by \'Sawera Ansari & Wasia Mukhtar Khan\'')

        menubar = Menu(self)
        self.config(menu=menubar)
        # Create the submenu
        subMenu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=subMenu)
        subMenu.add_command(label="Open", command=browse_file)

        def extended_playlist_menu(fl_name, name, option_menu):
            option_menu.add_command(label=fl_name, command=lambda pl_file_name=name: upload_playlist(name))
            option_menu.add_command(label='Delete playlist', command=lambda pl_file_name=name: del_playlist(name))

        def saved_menu():
            sved_pl = []
            for names in os.listdir():
                if names[-4:] == '.txt':
                    sved_pl += [names]

            if sved_pl != []:
                for name in sved_pl:
                    fl_name = name[:len(name) - 4]
                    option_menu=Menu(saved_playlist_menu, tearoff=0)
                    saved_playlist_menu.add_cascade(label=fl_name, menu=option_menu)
                    extended_playlist_menu(fl_name, name, option_menu)

            else:
                saved_playlist_menu.add_command(label='none')

        def refresh():
            '''Deletes the names of all the saved playlists from the menu and loads them again from saved_menu() method.
            This method takes care that if the user saves a new playlist while using the application then its name is also
            included in the menu when next time the user opens the menu.'''
            saved_playlist_menu.delete(0, 'end')
            saved_menu()

        upload_menu = Menu(subMenu, tearoff=0)
        saved_playlist_menu = Menu(upload_menu, tearoff=0, postcommand=refresh)     # postcommand -> method given in this parameter is executed each time the menu is opened.
        subMenu.add_cascade(label='Upload', menu=saved_playlist_menu)

        subMenu.add_command(label="Exit", command=self.on_closing)
        subMenu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=subMenu)
        subMenu.add_command(label="About Us", command=about_us)


exmple = MainGUI()
