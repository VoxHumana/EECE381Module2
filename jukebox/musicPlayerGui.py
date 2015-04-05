from subprocess import call

import RPi.GPIO as GPIO
from Tkinter import *
import tkFileDialog
import Tkinter
import tkFont
import Tkinter as tk
#import tkSnack
import os
import glob
import errno
import shlex

import vlc

music = vlc.MediaPlayer()

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

buffer0 = 21
buffer1 = 20
buffer2 = 16
buffer3 = 12
buffer4 = 26
buffer5 = 19
buffer6 = 13
buffer7 = 6

DE2flag = 23
PIflag = 24

GPIO.setup(buffer0, GPIO.IN)
GPIO.setup(buffer1, GPIO.IN)
GPIO.setup(buffer2, GPIO.IN)
GPIO.setup(buffer3, GPIO.IN)
GPIO.setup(buffer4, GPIO.IN)
GPIO.setup(buffer5, GPIO.IN)
GPIO.setup(buffer6, GPIO.IN)
GPIO.setup(buffer7, GPIO.IN)
GPIO.setup(DE2flag, GPIO.IN)
GPIO.setup(PIflag, GPIO.OUT)

#GPIO.add_event_detect(DE2flag, GPIO.RISING, callback=interrupt, bouncetime=50)

bass_band_1 = shlex.split("sudo amixer -D equal cset numid=1")
treble_band_1 = shlex.split("sudo amixer -D equal cset numid=8")

play_list_window = None

class playmusic:
	#GPIO.add_event_detect(DE2flag, GPIO.RISING, callback=interrupt, bouncetime=50)
	def __init__(self):
		global music
		global play_list_window
		
		self.root=tk.Tk()		

		self.root.title("Jukebox Music Player")
	
		self.root.configure(background = 'black')
		self.root.geometry('500x250+750+300')
		
		top = Frame(self.root)
		center = Frame(self.root)
		bottom = Frame(self.root)
		top.pack(side=TOP, fill = BOTH, expand = True)
		center.pack(side=TOP, fill = BOTH, expand = True)
		bottom.pack(side= BOTTOM, fill =BOTH, expand = True)
	
		self.filename = Tkinter.StringVar()
		self.name = Tkinter.StringVar()
		self.play_list = Tkinter.StringVar()
		
		title = Label(top, text ="Jukebox Music Player", fg='white', bg='RoyalBlue4')
		title.pack(in_=top, fill=BOTH, expand =True)

		play_list_window = Listbox(self.root, fg='white', bg='SteelBlue4')
		play_list_window.pack(in_=center, fill = BOTH, expand = True)
	
		play_button = Button(bottom, width = 5, height = 1, text = 'Play',
			fg='white', command = self.play, bg="DodgerBlue4")

		stop_button = Button(bottom, width = 5, height = 1, text = 'Stop',
                fg='white', command = self.stop, bg="SpringGreen4")
	        pause_button = Button(bottom, width = 5, height = 1, text = 'Pause',
	                fg='white', command = self.pause, bg="DodgerBlue4")
		play_list_window.insert(END, "0")
		
		play_button.pack(in_=bottom,side=LEFT, fill = BOTH, expand = True)
		pause_button.pack(in_=bottom,side=LEFT, fill = BOTH, expand = True)
		stop_button.pack(in_=bottom,side=LEFT, fill = BOTH, expand = True)
		play_list_window.bind('<Button-1>', callback)
		self.move()
		#self.getcommand()
		GPIO.add_event_detect(DE2flag, GPIO.RISING, callback=interrupt, bouncetime=50)	
		self.root.mainloop()
	 	
	def play(self):
		global music
		music.stop()
		music.play()
	def stop(self):
		global music
                music.stop()
		
        def pause(self):
		global music
                music.pause()
				

	def move(self):
		global play_list_window
	        path = '/home/pi/Desktop/jukebox/*.m4a'
       	 	files = glob.glob(path)
		index = play_list_window.size()
		songs = play_list_window.get(0, index-1)
		
        	for name in files:
			f=open(name)
			x = os.path.basename(f.name)
			if x in songs:
			 	string = "no"
			else:
        			play_list_window.insert(END, x)
		self.root.after(100,self.move)
	
	#def getcommand(self):
		#path = '/home/pi/Desktop/jukebox/commands.txt'
		#f = open(path)
		#data = f.read()
		#data = 'A'
		#if data=='A':
		#	print data
def receive():
	GPIO.output(PIflag, GPIO.LOW)
	while GPIO.input(DE2flag) == GPIO.LOW:
		pass
	received = GPIO.input(buffer0)
	received = received << 1
	received = received|GPIO.input(buffer1)
	received = received << 1
	received = received|GPIO.input(buffer2)
	received = received << 1
	received = received|GPIO.input(buffer3)
	received = received << 1
	received = received|GPIO.input(buffer4)
	received = received << 1
	received = received|GPIO.input(buffer5)
	received = received << 1
	received = received|GPIO.input(buffer6)
	received = received << 1
	received = received|GPIO.input(buffer7)
	GPIO.output(PIflag, GPIO.HIGH)
	while GPIO.input(DE2flag) == GPIO.HIGH:
		pass
	GPIO.output(PIflag, GPIO.LOW)
	return received

def interrupt(channel):
	idChar = chr(receive())
	print idChar
	if idChar == 'A':
		amp_value = receive()
		print amp_value
		cmd = bass_band_1
		cmd.append(str(amp_value))
		print cmd
		call(cmd)
		cmd.pop()

	elif idChar == 'B':
		amp_value = receive()
		print amp_value
		cmd = treble_band_1
		cmd.append(str(amp_value))
		print cmd
		call(cmd)
		cmd.pop()
							
def callback(event):
		global music
		music.stop()
		widget = event.widget
		selection = widget.curselection()
		value = widget.get(selection[0])
		value = os.path.basename(value)
		print value
		music = vlc.MediaPlayer(value)
	
if __name__== "__main__":
	playmusic()
	
