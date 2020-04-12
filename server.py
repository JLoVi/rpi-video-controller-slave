#!/usr/bin/env python3

import socket
import json
from screen_controller_class import ScreenController

HOST = '172.168.0.3'
PORT = 5000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((HOST, PORT))
s.listen(5)
sc = ScreenController();
while True:
	conn, addr = s.accept()
	print('Connected by', addr)
	data = conn.recv(1024)
	y = json.loads(data)
	message = y["message"]
	if message == "START_PLAYLIST":
		print('starting playlist')
		playlist_ids = y["ids"]
		sc.start_playlist(playlist_ids);
	elif message == "STOP_PLAYLIST":
		print('stop playlist')
	elif message == "START_STREAM":
		print('starting stream')
		i = y["id"]
		sc.start_stream(i)
	elif message == "STOP_STREAM":
		print('stop stream')
		sc.stop_stream()
	else:
		print('DO NOTHING BITCH')
		
	#if not data:
		#break
	#conn.sendall(data)
