#!/usr/bin/env python3
import socket
import json


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '127.0.0.1'
port = 1234
obj = {
	'sucess': True
}

message = json.dumps(obj)
s.connect((host, port))
s.sendall(bytes(message, encoding="utf-8"))
s.close()
