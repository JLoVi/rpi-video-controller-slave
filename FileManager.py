#!/usr/bin/env python3
import requests
import json
class FileManager:
	baseUrl = ""
	
	def __init__(self):
		self.baseUrl = "https://v2lu4dcv0l.execute-api.us-east-1.amazonaws.com/dev/"
		
	def set_videos(self, videos):
		video_string = json.dumps(videos)
		f = open("videos.json", "w")
		f.write(video_string)
		f.close()
		
	def set_screens(self, screens):
		screen_string = json.dumps(screens)
		f = open("screens.json", "w")
		f.write(screen_string)
		f.close()
		
	def get_videos(self):
		f = open("videos.json", "r")
		return f.write()

	def get_screens(self):
		f = open("screens.json", "r")
		return f.write()
