#!/usr/bin/env python3

import mpv
import json
from video_file import VideoFile
from pathlib import Path
from time import sleep
import logging
logging.basicConfig(level=logging.INFO)

stream_dict = {
	"569ad6dd-9c38-4a3b-955e-ce6ef935f31b": 3,
	"c4899b9f-1ddb-4929-b5b8-37c0f8fbee88": 2,
	"807ad9e3-2cc8-440f-bd63-3966725a5f9b": 1
}

class DisplayController:
	video_player_1 = None
	video_player_2 = None
	stream_player_1 = None
	stream_player_2 = None
	stream_player_3 = None
	fullscreen_player = None
	live_stream_players = [1, 2, 3]
	baseUrl = "http://10.0.0.111:8080/video/"
	def __init__(self):
		self.setup_live_stream_players()
		print('INIT')
		
	def setup_live_stream_players(self):
		for stream_player_id in self.live_stream_players:
			self.setup_stream_player(stream_player_id)
	
	def preload_live_stream_players(self):
		for stream_player_id in self.live_stream_players:
			self.start_stream_on_player(stream_player_id)
			
	def setup_stream_player(self, player):
		mpv_player = mpv.MPV(length="10", autofit="100%x100%", demuxer_thread="no", osc="no", border=False, fps="60", ontop=False, profile="low-latency", cache="no", untimed="yes", rtsp_transport="tcp", aid="no", input_vo_keyboard=True, brightness="0")
		if player == 1:
			self.stream_player_1 = mpv_player
		elif player == 2:
			self.stream_player_2 = mpv_player
		elif player == 3:
			self.stream_player_3 = mpv_player
	
	def load_video_players(self):
		self.setup_video_player(1)
		self.setup_video_player(2)
		self.video_player_1.play('test.mp4')
		self.video_player_2.play('test.mp4')
	
	def start_stream_on_player(self, stream_player_id):
		url = "rtsp://admin:false.memory@192.168.0.254/h264/ch1/main/av_stream"
		if stream_player_id == 1:
			self.stream_player_1.play(url)
		elif stream_player_id == 2:
			self.stream_player_2.play(url)
		elif stream_player_id == 3:
			self.stream_player_3.play(url)
			
	def setup_video_player(self, player):
		mpv_player = mpv.MPV(border=False, ontop=False, geometry="50%x50%", loop_file="no", length="10")
		#mpv_player.fullscreen = True
		if player == 1:
			self.video_player_1 = mpv_player
		elif player == 2:
			self.video_player_2 = mpv_player
		
	def set_player_one_fullscreen(self):
		sleep(3)
		self.video_player_1.fullscreen = True
			
	def start_stream(self, stream_id):
		#videos = json.load(open('videos.json', 'r'))
		#video = next((item for item in videos if item["id"] == stream_id), None)
		#url = video.uri
		url = "rtsp://admin:false.memory@192.168.0.254/h264/ch1/main/av_stream"
		player_id = stream_dict[stream_id]
		self.show_stream_player(player_id)
		#self.setup_stream_player(1)
		#self.stream_player_1.play(url)
		#self.stream_player_1.wait_for_playback()
		
	def show_stream_player(self, stream_player_id):
		if stream_player_id == 1:
			self.stream_player_1.fullscreen = True
		elif stream_player_id == 2:
			self.stream_player_2.fullscreen = True
		elif stream_player_id == 3:
			self.stream_player_3.fullscreen = True
		
	def start_video(self, video_id):
		url = self.baseUrl + video_id
		print(url)
		# check if player is already playing
		# if it is playing then fade out player 1 
		# start player 2 with new video fading in
		# quit player 1
		# do the same for player 2
		#url = "test.mp4"
		if self.video_player_1 == None:
			self.setup_video_player(1)
			#self.player1 = mpv.MPV(border=False, ontop=True)
			self.video_player_1.play(url)
			self.video_player_1.wait_for_playback()
			self.video_player_2 = None
		else:
			self.setup_video_player(2)
			self.video_player_2.play(url)
			self.video_player_2.wait_for_playback()
			self.video_player_1 = None
			
