#!/usr/bin/env python3
import websocket
import json
from EWSMessageType import EWSMessageType 
from EWSClientType import EWSClientType
from screen_controller_class import ScreenController
from RequestManager import RequestManager
from FileManager import FileManager

try:
    import thread
except ImportError:
    import _thread as thread
import time

rm = RequestManager()
fm = FileManager()
sc = ScreenController()
HOST = "wss://cs70esocmi.execute-api.us-east-1.amazonaws.com/dev"


def on_message(ws, message):
	print(message, 5)
	if message["message"] == EWSMessageType.START_PLAYLIST.name:
	    print('START_PLAYLIST')
	elif message["message"] == EWSMessageType.START_AUDIO.name:
	    print("START_AUDIO")
	elif message["message"] == EWSMessageType.START_SCHEDULE.name:
	    print("START_SCHEDULE")
	elif message["message"] == EWSMessageType.START_STREAM.name:
	    print("START_STREAM")
	elif message["message"] == EWSMessageType.START_VIDEO.name:
	    print("START_VIDEO")
	elif message["message"] == EWSMessageType.STOP_STREAM.name:
	    print("STOP_STREAM")
	else:
	    print("HELLO")

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    def run():
	message_object = {
	    "message": EWSMessageType.INITIALISE.name,
	    "client_type": EWSClientType.DISPLAY.name,
	    "raspberry_pi_id": 3
	}
	message_string = json.dumps(message_object)
	# Make Request for Videos and Screens
	videos = rm.get_videos()
	screens = rm.get_screens()
	
	# Store Videos In Json file
	fm.set_videos(videos)
	fm.set_screens(screens)
	
	# Find Screen
	screen = next((item for item in screens if item["raspberry_pi_id"] == "3"), None)
	playlist = screen['video_file_playlist']
	sc.start_playlist(playlist)
	
	# Send Message To Server
        ws.send(message_string)
    thread.start_new_thread(run, ())

def sort_videos(video):
    return video['order']

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(HOST,
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()
