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
	index = None
	def __init__(self):
		self.video_playlist = [VideoFile(1, "/media/pi/TOSHIBA1/Apocalyptic.mp4"), VideoFile(2, "/media/pi/TOSHIBA1/ledtime.mp4")]
		self.index = 0
		self.player_log = logging.getLogger("Player")	
	
	def setup_player_one(self):
		self.player1 = OMXPlayer(self.video_playlist[self.index].path, args='--win 0,0,1920,1080 --layer 2', bus_address_finder = None, Connection= None, dbus_name='orb.mpris.MediaPlayer2.omxplayer1', pause = True)
		self.player1.playEvent += lambda _: self.player_log.info(" 1 Play")
		self.player1.pauseEvent += lambda _: self.player_log.info("1 Pause")
		self.player1.stopEvent += lambda _: self.player_log.info("1 Stop")
		
	def setup_player_two(self):
		self.player2 = OMXPlayer(self.video_playlist[self.index + 1].path, args='--win 0,0,1920,1080 --layer 3', bus_address_finder = None, Connection= None, dbus_name='orb.mpris.MediaPlayer2.omxplayer2', pause = True)
		self.player2.playEvent += lambda _: self.player_log.info(" 2 Play")
		self.player2.pauseEvent += lambda _: self.player_log.info("2 Pause")
		self.player2.stopEvent += lambda _: self.player_log.info("2 Stop")
	
	def start_playlist(self):
		self.setup_player_one();
		self.setup_player_two();
		self.play_videos();
	
	def play_videos(self):
		alpha1 = 255
		self.player1.load(self.video_playlist[self.index].path, True)
		self.player2.load(self.video_playlist[self.index + 1].path, True)

		self.player1.play()
		while self.is_nearly_finished(self.player1) == False:
			sleep(1)
			
		#while self.is_nearly_finished(self.player1) == True and alpha1 > 0:
			#reductionRate = self.get_remaining_seconds(self.player1)
			#alpha1 = alpha1 - reductionRate
			#self.player1.set_alpha(alpha1)
			#sleep(1)
		
		self.player2.play()
		self.player1.stop()
		
		while self.is_nearly_finished(self.player2) == False:
			sleep(1)                
		self.player2.stop()
    
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
