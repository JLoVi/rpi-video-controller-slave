from omxplayer.player import OMXPlayer
from time import sleep
import os

curMovie = 0
p = []
playlist_file = open("playlist.txt")
movie = playlist_file.read().split("\n")
path = "/home/pi/projects/python-scrn-controller/"

class videoPlayer:
	def __init__(self, videoPath):
		self.videoPath = videoPath
		self.classPlayer = OMXPlayer(self.videoPath)
		sleep(0.2)
		self.classPlayer.pause()
		
	def playVideo(self):
		self.classPlayer.play()
		
	def end(self):
		return self.classPlayer.is_playing()
		
	def length(self):
		return self.classPlayer.duration()
	
	def freeze(self):
		self.classPlayer.quit()
		
for i in range(len(movie)):
	p[i].playVideo()
	sleep(p[i].length())
	p[i].stop()


