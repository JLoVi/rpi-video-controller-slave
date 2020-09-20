#!/usr/bin/env python3
import sys
import socket
import mpv
import threading
import json
from EWSMessageType import EWSMessageType
from EWSClientType import EWSClientType
from RequestManager import RequestManager
from FileManager import FileManager

rm = RequestManager()
fm = FileManager()

class PlaybackController:
	main_player = None
	
	## Display details
	pi_id = "3"
	orientation = "LANDSCAPE"
	
	index = 0
	actions = []
	
	baseUrl = "http://10.0.0.111:8080/video/"
	
	## Socket Server
	server = None
	host = '127.0.0.1'
	port = 1234
	
	## Playlists
	playlist = []
	playlist_index = 0
	
	def __init__(self):
		print('INIT')
		self.make_requests()

	def make_requests(self):
		# Make Request for Videos and Screens
		videos = rm.get_videos()
		screens = rm.get_screens()
		schedule = rm.get_schedule()
        # Store Videos In Json file
		fm.set_videos(videos)
		fm.set_screens(screens)
		fm.set_schedule(schedule)
	
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
	
	def setup_video_player(self):
		self.main_player = mpv.MPV(border=False, ontop=False, osc="yes", loop_file="yes", aid="no")

	def set_actions(self, schedule_actions):
		self.actions = list(filter(self.filter_actions, schedule_actions))

		for action in self.actions:
			self.playlist.append(self.baseUrl + action['PAYLOAD'])
		
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

			if is_schedule == True:	
				self.start_scheduled_video()
			else:
				self.start_single_video(video_id, is_schedule)
			
		elif obj['message'] == EWSMessageType.START_SCHEDULE.name:
			print('START_SCHEDULE')
			self.start_schedule()
		
		elif obj['message'] == EWSMessageType.STOP_SCHEDULE.name:
			print('STOP_SCHEDULE')
			self.stop_schedule()
			
	def start_schedule(self):
		schedule_actions = fm.get_schedule()
		self.set_actions(schedule_actions)

	def stop_schedule(self):
		screens = fm.get_screens()
		screen = next(
			(item for item in screens if item["raspberry_pi_id"] == pi_id),
		None)
		video_id = screen['video_id']
		is_schedule = False
		self.start_single_video("4ef1e328-1ce7-4e3a-9979-30ee84f38856", is_schedule)

	def setup_playlist(self):
		if self.main_player == None:	
			self.setup_video_player()
		
		for vid in self.playlist:
			self.main_player.playlist_append(vid)
		
		self.main_player.playlist_pos = 0
	
	def clear_playlist(self):
		self.playlist = []
		self.playlist_index = 0
		self.main_player.playlist_clear()
		
		
	def start_scheduled_video(self):
		if self.playlist_index == 0:
			self.setup_playlist()
		else:
			self.main_player.playlist_next()
			
		self.playlist_index = self.playlist_index + 1
		
	def start_single_video(self, video_id, schedule):
		url = self.baseUrl + video_id
		print('MAIN PLAYER IS 1')
		if self.main_player == None:
			self.setup_video_player()
		
		self.main_player.play(url)


if __name__ == "__main__":
	playback_controller = PlaybackController()
	pi_id = str(3)
	orientation = "LANDSCAPE"
	if len(sys.argv) > 1:
		pi_id = str(sys.argv[1])
		if len(sys.argv) > 2:
			orientation = sys.argv[2]
	
	playback_controller.set_pi_id(pi_id)
	playback_controller.set_orientation(orientation)
		
	x = threading.Thread(target=playback_controller.start_single_video, args=("5efab20a-2112-4f59-967e-d0ef442c74a1", False))
	y = threading.Thread(target=playback_controller.setup_server, args = ())
	x.start()
	y.start()
