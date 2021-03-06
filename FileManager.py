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
		
	def set_schedule(self, schedule):
		schedule_string = json.dumps(schedule)
		f = open('schedule.json', 'w')
		f.write(schedule_string)
		f.close()
			
		
	def get_videos(self):
		f = open("videos.json", "r")
		videos = json.loads(f.read())
		return videos

	def get_screens(self):
		f = open("screens.json", "r")
		screens = json.loads(f.read())
		return screens
		
	def get_schedule(self):
		f = open("schedule.json", "r")
		schedule = json.loads(f.read())
		return schedule
