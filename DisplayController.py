#!/usr/bin/env python3
import sys
import socket
import mpv
import threading
import json
from video_file import VideoFile
from pathlib import Path
from time import sleep
import logging
from RequestManager import RequestManager
from FileManager import FileManager
from EWSMessageType import EWSMessageType
logging.basicConfig(level=logging.INFO)

stream_dict = {
	"569ad6dd-9c38-4a3b-955e-ce6ef935f31b": 3,
	"c4899b9f-1ddb-4929-b5b8-37c0f8fbee88": 2,
	"807ad9e3-2cc8-440f-bd63-3966725a5f9b": 1
}

rm = RequestManager()
fm = FileManager()

class DisplayController:
	fullscreen_player = None
	fullscreen_player_index = None
	main_player_1 = None
	main_player_2 = None
	pi_id = "3"
	orientation = "LANDSCAPE"
	
	index = 0
	actions = []
	
	baseUrl = "http://10.0.0.111:8080/video/"
	
	server = None
	host = '127.0.0.1'
	port = 1234
	
	def __init__(self):
		print('INIT')
		#self.make_requests()

	def make_requests(self):
		# Make Request for Videos and Screens
		print('STARTED REQUESTS')
		videos = rm.get_videos()
		screens = rm.get_screens()
		schedule = rm.get_schedule()
        
        # Store Videos In Json file
		fm.set_videos(videos)
		fm.set_screens(screens)
		fm.set_schedule(schedule)
		print('ENDED REQUESTS')
	
	def setup_server(self):
		server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		server.bind((self.host, self.port))
		server.listen()
		print('SERVER UP')
		while True:
			c, addr = server.accept()
			data = c.recv(1024)
			decoded_data = data.decode('utf-8')
			self.respond_to_socket_message(decoded_data)
			c.close()
	
	def respond_to_socket_message(self, message):
		obj = json.loads(message)
		if obj['message'] == EWSMessageType.START_VIDEO.name:
			print('START_VIDEO')
			video_id = ""
			is_schedule = False
			if obj['payload'] is None:
				screens = fm.get_screens()
				screen = next(
					(item for item in screens if item["raspberry_pi_id"] == pi_id),
				None)
				video_id = screen['video_id']
				is_schedule = False
			else:
				video_id = obj['payload']
				is_schedule = True
			self.start_video(video_id, is_schedule)
			print('video', video_id)
			print('is_schedule', is_schedule)
			
		elif obj['message'] == EWSMessageType.START_STREAM.name:
			print('START_STREAM')
			self.start_stream(obj['payload'])
			
		elif obj['message'] == EWSMessageType.START_SCHEDULE.name:
			print('START_SCHEDULE')
			self.start_schedule()
		
	def start_schedule(self):
		schedule_actions = fm.get_schedule()
		self.set_actions(schedule_actions)
		self.setup()
		
	def set_actions(self, schedule_actions):
		self.actions = list(filter(self.filter_actions, schedule_actions))
		
	def set_pi_id(self, pi_id):
		self.pi_id = pi_id
	
	def set_orientation(self, orientation):
		if orientation == "LANDSCAPE":
			self.orientation = orientation
		elif orientation == "PORTRAIT":
			self.orientation = orientation
			
	def filter_actions(self, action):
		if action['RPI_ID'] == self.pi_id:
			return True
		else:
			return False
	
	def setup(self):
		action = self.actions[self.index]
		if action['ACTION'] == EWSMessageType.START_VIDEO.name:
			if self.fullscreen_player_index == 1:
				self.setup_video_player(2)
			else:
				self.setup_video_player(1)
		elif action['ACTION'] == EWSMessageType.START_STREAM.name:
			if self.fullscreen_player_index == 1:
				self.load_stream_player(self.main_player_2)
				self.start_stream_on_player(2, action['PAYLOAD'])
			else:
				self.load_stream_player(self.main_player_1)
				self.start_stream_on_player(1, action['PAYLOAD'])
	
	def load_next_action_for_player(self, player):
		self.increment_index()
		if self.index + 1 >= len(self.actions):
			return
		else:	
			action = self.actions[self.index]
			print('load_next_action_for_player', player)
			if action['ACTION'] == EWSMessageType.START_VIDEO.name:
				if self.fullscreen_player_index == 1:
					self.setup_video_player(2)
				else:
					self.setup_video_player(1)
			elif action['ACTION'] == EWSMessageType.START_STREAM.name:
				print('LOAD STREAM PLAYER')
				if self.fullscreen_player_index == 1:
					self.load_stream_player(self.main_player_2)
					self.start_stream_on_player(2, action['PAYLOAD'])
				else:
					self.load_stream_player(self.main_player_1)
					self.start_stream_on_player(1, action['PAYLOAD'])
		
	def increment_index(self):
		self.index = self.index + 1
		
	def load_stream_player(self, player):
		mpv_player = mpv.MPV(vf="crop=600:1080:500:0", geometry="+960+0", speed="1.1", no_correct_pts="yes", demuxer_thread="no", osc="yes", border=False, fps="60", ontop=False, profile="low-latency", cache="no", untimed="yes", rtsp_transport="tcp", aid="no", input_vo_keyboard=True, brightness="0")
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
			
	def setup_video_player(self, player_id):
		mpv_player = mpv.MPV(border=False, ontop=False, osc="yes", loop_file="no", aid="no")
		if player_id == 1:
			self.main_player_1 = mpv_player
		elif player_id == 2:
			self.main_player_2 = mpv_player
			
	def start_stream(self, stream_id):
		#videos = json.load(open('videos.json', 'r'))
		#video = next((item for item in videos if item["id"] == stream_id), None)
		#url = video.uri
		url = "rtsp://admin:false.memory@192.168.0.254/h265/ch1/main/av_stream"
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
		
	def start_video(self, video_id, schedule):
		url = self.baseUrl + video_id
		print(url)
		#url = "test.mp4"
		if self.fullscreen_player_index == 1:
			print('MAIN PLAYER IS 1')
			self.main_player_2.play(url)
			self.set_fullscreen_player(self.main_player_2, 2)
			if schedule == True:
				self.load_next_action_for_player(1)
		elif self.fullscreen_player_index == 2:
			print('MAIN PLAYER IS 2')
			self.main_player_1.play(url)
			self.set_fullscreen_player(self.main_player_1, 1)
			if schedule == True:
				self.load_next_action_for_player(2)
		elif self.fullscreen_player == None:
			print('JUST STARTING PLAYER')
			self.setup_video_player(1)
			self.main_player_1.play(url)
			print('PLAY VIDEO')
			self.set_fullscreen_player(self.main_player_1, 1)
			self.main_player_1.wait_for_playback()
			if schedule == True:
				self.load_next_action_for_player(2)
	
	def set_fullscreen_player(self, player, index):
		previous_fullscreen_player = self.fullscreen_player
		self.fullscreen_player = player
		self.fullscreen_player_index = index
		if index == 1:
			self.main_player_1.fullscreen = True
		elif index == 2:
			self.main_player_2.fullscreen = True

		if previous_fullscreen_player != None:
			if index == 1:
				self.main_player_2.fullscreen = False
			elif index == 2:
				self.main_player_1.fullscreen = False
		
if __name__ == "__main__":
	dc = DisplayController()
	pi_id = str(3)
	orientation = "LANDSCAPE"
	if len(sys.argv) > 1:
		pi_id = str(sys.argv[1])
		if len(sys.argv) > 2:
			orientation = sys.argv[2]
	
	dc.set_pi_id(pi_id)
	dc.set_orientation(orientation)
		
	x = threading.Thread(target=dc.start_video, args=("4ef1e328-1ce7-4e3a-9979-30ee84f38856", False))
	y = threading.Thread(target=dc.setup_server, args = ())
	x.start()
	y.start()

			

