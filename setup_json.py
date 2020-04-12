#!/usr/bin/env python3

import json

files = {
	"1": "/media/pi/TOSHIBA1/Apocalyptic.mp4",
	"2": "/media/pi/TOSHIBA1/ledtime.mp4",
	"3": "/media/pi/TOSHIBA1/DiscoLightsVidevo.mov"
}

streams = {
	"1" : "rtsp://admin:false.memory@192.168.0.25/h264/ch1/main/av_stream"
}

json_file = json.dumps(files)

f = open("videos.json", "w")
f.write(json_file)
f.close()

json_stream = json.dumps(streams)

s = open("streams.json", "w")
s.write(json_stream)
s.close()
