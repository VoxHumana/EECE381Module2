import subprocess


from Tkinter import *
import tkFileDialog
import Tkinter
import tkFont
import Tkinter as tk
import tkSnack
import vlc
import os
import glob
import errno

music = vlc.MediaPlayer()

class playmusic:
	def __init__(self):
		global music
		
		self.root=tk.Tk()		
		tkSnack.initializeSnack(self.root)


		self.root.title("Jukebox Music Player")
	
		self.root.configure(background = 'black')
		self.root.geometry('500x250+750+300')
	
		self.filename = Tkinter.StringVar()
		self.name = Tkinter.StringVar()
		self.play_list = Tkinter.StringVar()
	
		play_button = Button(self.root, width = 5, height = 1, text = 'Play',
			fg='white', command = self.play, bg="black")
		play_button.grid(row=0, column=0, stick=W)
		
		stop_button = Button(self.root, width = 5, height = 1, text = 'Stop',
                fg='white', command = self.stop, bg="black")
	        stop_button.grid(row=0, column=1, stick=W)
	
	        pause_button = Button(self.root, width = 5, height = 1, text = 'Pause',
	                fg='white', command = self.pause, bg="black")
	        pause_button.grid(row=0, column=2)

	
	        self.volume_slider = Scale(self.root, label = 'Volume', 
			orient = 'horizontal',fg='white', 
			 bg="black")
	        self.volume_slider.grid(row=0, column=4)
	
		play_list_window = Toplevel(self.root, height = 150, width = 100)
		play_list_window.title("Playlist")
		self.play_list_display = Listbox(play_list_window, selectmode=EXTENDED, 
		width = 50, bg = "Dark Slate grey", fg = "white")
		self.play_list_display.insert(END, "0")
		self.play_list_display.pack()
		play_list_window.bind('<Button-1>', callback)
		self.move()		
		play_list_window.mainloop()
		self.root.mainloop()
	 	
	def play(self):
		global music
		music.play()
	def stop(self):
		global music
		music.stop()

        def pause(self):
		global music
		music.pause()

	def move(self):
	        path = '/home/pi/Desktop/jukebox/*.mp3'
       	 	files = glob.glob(path)
		index = self.play_list_display.size()
		songs = self.play_list_display.get(0, index-1)
		
        	for name in files:
			f=open(name)
			if f.name in songs:
			 	string = "no"
			else:
        			self.play_list_display.insert(END, f.name)
		self.root.after(100,self.move)
					
def callback(event):
		global music
		music.stop()
		widget = event.widget
		selection = widget.curselection()
		value = widget.get(selection[0])
		music = vlc.MediaPlayer(value)
	
	
if __name__== "__main__":
	playmusic()
	
