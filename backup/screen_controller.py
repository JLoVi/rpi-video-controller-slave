#!/usr/bin/env python3

from omxplayer.player import OMXPlayer
from pathlib import Path
from time import sleep
import logging
logging.basicConfig(level=logging.INFO)

VIDEO1_PATH = Path("/media/pi/TOSHIBA1/Apocalyptic.mp4")
VIDEO2_PATH = Path("/media/pi/TOSHIBA1/ledtime.mp4")
player_log = logging.getLogger("Player")

player1 = OMXPlayer(VIDEO1_PATH, args='--win 0,0,1920,1080 --layer 2', bus_address_finder = None, Connection= None, dbus_name='orb.mpris.MediaPlayer2.omxplayer1', pause= True)
player1.set_alpha(200);
player1.playEvent += lambda _: player_log.info(" 1 Play")
player1.pauseEvent += lambda _: player_log.info("1 Pause")
player1.stopEvent += lambda _: player_log.info("1 Stop")


player2 = OMXPlayer(VIDEO2_PATH, args='--layer 1', bus_address_finder = None, Connection= None, dbus_name='orb.mpris.MediaPlayer2.omxplayer2', pause= True)
player2.playEvent += lambda _: player_log.info(" 2 Play")
player2.pauseEvent += lambda _: player_log.info("2 Pause")
player2.stopEvent += lambda _: player_log.info("2 Stop")

player2.play()
player1.play()

alpha = 200
for x in range(50):
	sleep(0.1)
	alpha = alpha - 5
	player1.set_alpha(alpha)
	
sleep(3)

player1.quit()
player2.quit()

