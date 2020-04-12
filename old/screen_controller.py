#!/usr/bin/env python3

from video_file import VideoFile
from omxplayer.player import OMXPlayer
from pathlib import Path
from time import sleep
import logging
logging.basicConfig(level=logging.INFO)

video_playlist = []
player1 = None
player2 = None

video_playlist = [VideoFile(1, "/media/pi/TOSHIBA1/Apocalyptic.mp4"), VideoFile(2, "/media/pi/TOSHIBA1/ledtime.mp4")]
player_log = logging.getLogger("Player")

player1 = OMXPlayer(video_playlist[0].path, args='--win 0,0,1920,1080 --layer 2', bus_address_finder = None, Connection= None, dbus_name='orb.mpris.MediaPlayer2.omxplayer1', pause= True)
player1.set_alpha(200);


player2 = OMXPlayer(video_playlist[1].path, args='--win 0,0,1920,1080 --layer 1', bus_address_finder = None, Connection= None, dbus_name='orb.mpris.MediaPlayer2.omxplayer2', pause= True)

player1.play()
sleep(player1.duration()-1)
alpha1 = 200

player2.pause()
for x in range(6):
	sleep(0.1)
	alpha1 = alpha1 - 20
	player1.set_alpha(alpha1)

player2.play()

