#!/usr/bin/env python3
import websocket
import socket
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


pi_id = str(3)

if len(sys.argv) > 1:
    pi_id = str(sys.argv[1])
    
    
rm = RequestManager()
fm = FileManager()

HOST = "wss://cs70esocmi.execute-api.us-east-1.amazonaws.com/dev"

def send_to_display_controller(message):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '127.0.0.1'
    port = 1234
    obj = {
        'success': True
    }

    message = json.dumps(obj)
    s.connect((host, port))
    s.sendall(bytes(message, encoding="utf-8"))
    s.close()

def on_open(ws):
    def run():
        message_object = {
            "message": EWSMessageType.INITIALISE.name,
            "client_type": EWSClientType.DISPLAY.name,
            "raspberry_pi_id": pi_id
        }
        message_string = json.dumps(message_object)
        
        #schedule_actions = fm.get_schedule()
        #dc.set_actions(schedule_actions)
        #dc.setup()
        # Send Message To Server
        ws.send(message_string)
    thread.start_new_thread(run, ())
    
def on_message(ws, message):
    message = json.loads(message)
    if message["message"] == EWSMessageType.START_PLAYLIST.name:
        screen = next(
            (item for item in screens if item["raspberry_pi_id"] == pi_id),
            None)
        playlist = screen['video_file_playlist']
    elif message["message"] == EWSMessageType.START_STREAM.name:
        print("START_STREAM")
        #dc.start_stream(message['payload'])
    elif message["message"] == EWSMessageType.START_VIDEO.name:
        print("START_VIDEO")
        video_id = ""
        is_schedule = False
        print(message)
        if message['payload'] is None:
            screens = fm.get_screens()
            screen = next(
                (item for item in screens if item["raspberry_pi_id"] == pi_id),
            None)
            video_id = screen['video_id']
            is_schedule = False
        else:
            video_id = message['payload']
            is_schedule = True
        send_to_display_controller(message)
        #dc.start_video(video_id, is_schedule)
    elif message["message"] == EWSMessageType.START_SCHEDULE.name:
        print("START_SCHEDULE")
        schedule_actions = fm.get_schedule()
        #dc.set_actions(schedule_actions)
        #dc.setup()
        #dc.preload_live_stream_players()
    elif message["message"] == EWSMessageType.STOP_SCHEDULE.name:
        print("STOP_SCHEDULE")
    else:
        print(message["message"])


def on_error(ws, error):
    print(error)


def on_close(ws):
    print("### closed ###")


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
