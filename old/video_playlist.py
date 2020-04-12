from omxplayer.player import OMXPlayer
import time

video_path = '/media/pi/TOSHIBA{}'
video_list = ['Apocalyptic.mp4', 'ledtime.mp4']
plrs = [None,None]
bus = ["org.mpris.MediaPlayer2.omxplayer2", "org.mpris.MediaPlayer2.omxplayer3",]

for i, vid in enumerate(video_list):
	ix = i % 2
	plrs[ix] = OMXPlayer(video_path.format(vid), args=['--layer', str((ix+1)%2)], dbus_name=bus[ix])
	print(plrs[ix].duration())
	time.sleep(plrs[ix].duration() - 0.5)
