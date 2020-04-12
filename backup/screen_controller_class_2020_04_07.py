#!/usr/bin/env python3

from video_file import VideoFile
from omxplayer.player import OMXPlayer
from pathlib import Path
from time import sleep
import logging
logging.basicConfig(level=logging.INFO)

class ScreenController:
	video_playlist = []
	player1 = None
	player2 = None
	index = None
	number_of_cycles = 0
	currentIndex = None
	nextIndex = None
	
	def __init__(self):
		self.video_playlist = [VideoFile(1, "/media/pi/TOSHIBA1/Apocalyptic.mp4"), VideoFile(2, "/media/pi/TOSHIBA1/ledtime.mp4"), VideoFile(3, "/media/pi/TOSHIBA1/DiscoLightsVidevo.mov")]
		self.index = 0
		self.currentIndex = 0
		self.nextIndex = self.currentIndex+1
		self.player_log = logging.getLogger("Player")	
	
	def setup_player_one(self):
		self.player1 = OMXPlayer(self.video_playlist[self.index].path, args='--win 0,0,1920,1080 --layer 2', dbus_name='orb.mpris.MediaPlayer2.omxplayer1', pause = True)
		self.player1.playEvent += lambda _: self.player_log.info(" 1 Play")
		self.player1.pauseEvent += lambda _: self.player_log.info("1 Pause")
		self.player1.stopEvent += lambda _: self.player_log.info("1 Stop")
		
	def setup_player_two(self):
		self.player2 = OMXPlayer(self.video_playlist[self.index + 1].path,  args='--win 0,0,1920,1080 --layer 1', dbus_name='orb.mpris.MediaPlayer2.omxplayer2', pause = True)
		self.player2.playEvent += lambda _: self.player_log.info(" 2 Play")
		self.player2.pauseEvent += lambda _: self.player_log.info("2 Pause")
		self.player2.stopEvent += lambda _: self.player_log.info("2 Stop")
	
	def start_playlist(self):
		self.setup_player_one();
		self.setup_player_two();
		self.play_videos(True);
	
	def play_videos(self, init = False):
		# Load players with appropiate indexes	
		self.player1.load(self.video_playlist[self.currentIndex].path, True)
		self.player2.load(self.video_playlist[self.nextIndex].path, True)
		
		self.player1.set_alpha(255)
		self.player2.set_alpha(255)
		# Play for total duration - 1 second	
		self.player1.play()
		sleep(self.player1.duration()-1)
		
		# Fade player 
		self.fade_player_out(self.player1)
		
		# Play for total duration - 1 second	
		self.player2.play()
		sleep(self.player2.duration()-1)
		
		# Set new current and next index 
		self.reset_indexes()
		
		# Recursively call play videos
		self.number_of_cycles = self.number_of_cycles + 1
		if(self.number_of_cycles < 2):
			self.play_videos(False)
			
		# Fade player
		self.fade_player_out(self.player2)



		

	
	def reset_indexes(self): 

		
		if self.nextIndex + 1 >= len(self.video_playlist):
			self.currentIndex = 0
		else :
			self.currentIndex = self.nextIndex + 1
			
		if self.currentIndex + 1 >= len(self.video_playlist):
			self.nextIndex = 0
		else:
			self.nextIndex = self.currentIndex + 1
		
		print('AFTER CURRENT')
		print(self.currentIndex)
		print('AFTER NEXT')
		print(self.nextIndex)
		
	def fade_player_out(self, player):
		alpha = 200
		for x in range(6):
			sleep(0.1)
			alpha = alpha - 20
			player.set_alpha(alpha)
			
		alpha = 200
	
	def get_remaining_seconds(self, player):
		remaining_seconds = player.duration() - player.position()
		return remaining_seconds
             
	def is_nearly_finished(self, player):
		amountPlayed = 0
		if player.position() > 0:
			amountPlayed = player.position();
		percentPlayed = amountPlayed/player.duration()
		print(percentPlayed)
		if(percentPlayed > 0.9):
			return True;
		else:
			return False;
		
sc = ScreenController();
sc.start_playlist(); 
