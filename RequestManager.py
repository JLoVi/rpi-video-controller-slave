#!/usr/bin/env python3
import requests
import json
class RequestManager:
	baseUrl = ""
	
	def __init__(self):
		self.baseUrl = "https://v2lu4dcv0l.execute-api.us-east-1.amazonaws.com/dev/"
		
	def get_videos(self):
		video_string = requests.get('http://10.0.0.111:8080/' + 'videos').text
		videos =json.loads(video_string)
		return videos

	def get_screens(self):
		screen_string = requests.get('http://10.0.0.111:8080/' + 'screens').text
		screens =json.loads(screen_string)
		return screens
	
	def get_schedule(self):
		schedule_string = requests.get('http://10.0.0.111:8080/schedule').text
		schedule = json.loads(schedule_string)
		return schedule
