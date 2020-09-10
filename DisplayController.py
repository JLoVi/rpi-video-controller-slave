#!/usr/bin/env python3

import mpv
import json
from video_file import VideoFile
from pathlib import Path
from time import sleep
import logging
from EWSMessageType import EWSMessageType
logging.basicConfig(level=logging.INFO)

stream_dict = {
	"569ad6dd-9c38-4a3b-955e-ce6ef935f31b": 3,
	"c4899b9f-1ddb-4929-b5b8-37c0f8fbee88": 2,
	"807ad9e3-2cc8-440f-bd63-3966725a5f9b": 1
}

class DisplayController:
	fullscreen_player = None
	fullscreen_player_index = None
	main_player_1 = None
	main_player_2 = None
	pi_id = "3"
	index = 0
	
	live_stream_players = [1, 2, 3]
	actions = []
	baseUrl = "http://10.0.0.111:8080/video/"
	def __init__(self):
		print('INIT')
		
	def set_actions(self, schedule_actions):
		self.actions = list(filter(self.filter_actions, schedule_actions))
		#for action in self.actions:
		#	print('ACTION', action)
		
	def set_pi_id(self, pi_id):
		self.pi_id = pi_id
	
	def filter_actions(self, action):
		if action['RPI_ID'] == self.pi_id:
			return True
		else:
			return False
	
	def setup(self):
		print('CALLED SETUP', self.actions)
		action = self.actions[self.index]
		if action['ACTION'] == EWSMessageType.START_VIDEO.name:
			self.setup_video_player(1)
		elif action['ACTION'] == EWSMessageType.START_STREAM.name:
			print('LOAD STREAM PLAYER')
			self.load_stream_player(self.main_player_1)
			self.start_stream_on_player(self.main_player_1, action['PAYLOAD'])
	
	def load_next_action_for_player(self, player):
		self.increment_index()
		action = self.actions[self.index]
		print('load_next_action_for_player', player)
		if action['ACTION'] == EWSMessageType.START_VIDEO.name:
			print('LOAD VIDEO PLAYER')
			self.setup_video_player(player)
		elif action['ACTION'] == EWSMessageType.START_STREAM.name:
			print('LOAD STREAM PLAYER')
			self.load_stream_player(player)
			self.start_stream_on_player(player, action['PAYLOAD'])
		
	def increment_index(self):
		self.index = self.index + 1
		
	def load_stream_player(self, player):
		mpv_player = mpv.MPV(length="60", autofit="100%x100%", demuxer_thread="no", osc="no", border=False, fps="60", ontop=False, profile="low-latency", cache="no", untimed="yes", rtsp_transport="tcp", aid="no", input_vo_keyboard=True, brightness="0")
		if player == 1:
			self.main_player_1 = mpv_player
		elif player == 2:
			self.main_player_2 = mpv_player
	
	def start_stream_on_player(self, stream_player_id, stream_id):
		url = "rtsp://admin:false.memory@192.168.0.254/h264/ch1/main/av_stream"
		if stream_player_id == 1:
			self.main_player_1.play(url)
		elif stream_player_id == 2:
			self.main_player_2.play(url)
			
	def setup_video_player(self, player):
		mpv_player = mpv.MPV(border=False, ontop=True, geometry="100%x100%", loop_file="no", aid="no")
		if player == 1:
			self.main_player_1 = mpv_player
		elif player == 2:
			self.main_player_2 = mpv_player
			
	def start_stream(self, stream_id):
		#videos = json.load(open('videos.json', 'r'))
		#video = next((item for item in videos if item["id"] == stream_id), None)
		#url = video.uri
		url = "rtsp://admin:false.memory@192.168.0.254/h264/ch1/main/av_stream"
		if self.fullscreen_player_index == 1:
			self.set_fullscreen_player(self.main_player_2, 2)
			self.load_next_action_for_player(1)
		elif self.fullscreen_player_index == 2:
			self.set_fullscreen_player(self.main_player_1, 1)
			self.load_next_action_for_player(2)
		elif self.fullscreen_player == None:
			self.video_player_1.play(url)
			self.set_fullscreen_player(self.main_player_1, 1)
			self.load_next_action_for_player(2)
		#player_id = stream_dict[stream_id]
		#print('PLAYER ID', player_id)
		#self.show_stream_player(player_id)
		#self.setup_stream_player(1)
		#self.stream_player_1.play(url)
		#self.stream_player_1.wait_for_playback()
		
	def start_video(self, video_id):
		url = self.baseUrl + video_id
		#url = "test.mp4"
		print('FULLSCREEN', self.fullscreen_player)
		print('main_player_1', self.main_player_1)
		if self.fullscreen_player_index == 1:
			print('MAIN PLAYER IS 1')
			self.main_player_2.play(url)
			self.set_fullscreen_player(self.main_player_2, 2)
			self.load_next_action_for_player(1)
		elif self.fullscreen_player_index == 2:
			print('MAIN PLAYER IS 2')
			self.main_player_1.play(url)
			self.set_fullscreen_player(self.main_player_1, 1)
			self.load_next_action_for_player(2)
		elif self.fullscreen_player == None:
			print('MAIN PLAYER IS 3')
			self.main_player_1.play(url)
			self.set_fullscreen_player(self.main_player_1, 1)
			self.load_next_action_for_player(2)
	
	def set_fullscreen_player(self, player, index):
		previous_fullscreen_player = self.fullscreen_player
		self.fullscreen_player = player
		self.fullscreen_player_index = index
		self.fullscreen_player.fullscreen = True
		if previous_fullscreen_player != None:
			previous_fullscreen_player.fullscreen = False
		
			
	def setup_live_stream_players(self):
		for stream_player_id in self.live_stream_players:
			self.setup_stream_player(stream_player_id)
	
	def preload_live_stream_players(self):
		for stream_player_id in self.live_stream_players:
			self.start_stream_on_player(stream_player_id)
			
	def setup_stream_player(self, player):
		mpv_player = mpv.MPV(length="60", autofit="100%x100%", demuxer_thread="no", osc="no", border=False, fps="60", ontop=False, profile="low-latency", cache="no", untimed="yes", rtsp_transport="tcp", aid="no", input_vo_keyboard=True, brightness="0")
		if player == 1:
			self.stream_player_1 = mpv_player
		elif player == 2:
			self.stream_player_2 = mpv_player
		elif player == 3:
			self.stream_player_3 = mpv_player
