#!/usr/bin/env python3

import mpv
import json
from video_file import VideoFile
from pathlib import Path
from time import sleep
import logging
logging.basicConfig(level=logging.INFO)

class DisplayController:
	player1 = None
	player2 = None
	baseUrl = "http://10.0.0.111:8080/video/"
	def __init__(self):
		print('INIT')
		
	def setup_stream_player(self, player):
		player = mpv.MPV(border=False, ontop=True, profile="low-latency", cache="no", untimed="no", rtsp_transport="tcp")
	
	def setup_video_player(self, player):
		player = mpv.MPV(border=False, ontop=True)
		
	def start_stream(self, stream_id):
		videos = json.load(open('videos.json', 'r'))
		video = next((item for item in videos if item["id"] == stream_id), None)
		url = video.uri
		url = "rtsp://admin:false.memory@192.168.0.254/h264/ch1/main/av_stream"
		self.setup_stream_player(self.player1)
		self.player1.play(url)
		
	def start_video(self, video_id):
		url = self.baseUrl + video_id
		print(url)
		# check if player is already playing
		# if it is playing then fade out player 1 
		# start player 2 with new video fading in
		# quit player 1
		# do the same for player 2
		#url = "test.mp4"
		if self.player1 == None:
			#self.setup_video_player(self.player1)
			self.player1 = mpv.MPV(border=False, ontop=True)
			self.player1.play(url)
			self.player1.wait_for_playback()
			self.player2 = None
		else:
			self.setup_video_player(self.player2)
			self.player2.play(url)
			self.player1 = None
			
