#!/usr/bin/env python3
import websocket
import json
import sys
from EWSMessageType import EWSMessageType
from EWSClientType import EWSClientType
from RequestManager import RequestManager
from FileManager import FileManager
from DisplayController import DisplayController

try:
    import thread
except ImportError:
    import _thread as thread
import time

rm = RequestManager()
fm = FileManager()
dc = DisplayController()
HOST = "wss://cs70esocmi.execute-api.us-east-1.amazonaws.com/dev"
pi_id = str(3)

if len(sys.argv) > 1:
    pi_id = str(sys.argv[1])


def on_message(ws, message):
    message = json.loads(message)
    if message["message"] == EWSMessageType.START_PLAYLIST.name:
        screen = next(
            (item for item in screens if item["raspberry_pi_id"] == pi_id),
            None)
        playlist = screen['video_file_playlist']
    elif message["message"] == EWSMessageType.START_STREAM.name:
        print("START_STREAM")
        dc.start_stream(message['payload'])
    elif message["message"] == EWSMessageType.START_VIDEO.name:
        print("START_VIDEO")
        video_id = ""
        print(message)
        if message['payload'] is None:
            screens = fm.get_screens()
            screen = next(
                (item for item in screens if item["raspberry_pi_id"] == pi_id),
            None)
            video_id = screen['video_id']
        else:
            video_id = message['payload']
        
        #dc.load_video_players()
        #dc.preload_live_stream_players()
        dc.start_video(video_id)
    elif message["message"] == EWSMessageType.START_SCHEDULE.name:
        print("START_SCHEDULE")
        dc.setup_live_stream_players()
        dc.preload_live_stream_players()
    elif message["message"] == EWSMessageType.STOP_STREAM.name:
        print("STOP_STREAM")
        #sc.stop_stream()
    else:
        print("NOT VALID")


def on_error(ws, error):
    print(error)


def on_close(ws):
    print("### closed ###")


def on_open(ws):
    def run():
        message_object = {
            "message": EWSMessageType.INITIALISE.name,
            "client_type": EWSClientType.DISPLAY.name,
            "raspberry_pi_id": pi_id
        }
        message_string = json.dumps(message_object)
        # Make Request for Videos and Screens
        videos = rm.get_videos()
        screens = rm.get_screens()

        # Store Videos In Json file
        fm.set_videos(videos)
        fm.set_screens(screens)

        # Find Screen
        screen = next(
            (item for item in screens if item["raspberry_pi_id"] == pi_id),
            None)
        playlist = screen['video_file_playlist']
        # sc.start_playlist(playlist)
        # sc.play_single_video("375caf5d-53ef-41ad-8d24-52ae8686620e")
        # Send Message To Server
        ws.send(message_string)
    thread.start_new_thread(run, ())


def sort_videos(video):
    return video['order']


if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(HOST,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()
