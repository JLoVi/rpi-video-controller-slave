#!/usr/bin/env python3
import mpv
player = mpv.MPV(border=False, ontop=True, video_latency_hacks="yes", profile="low-latency", cache="no", untimed="no", rtsp_transport="tcp")
#player = mpv.MPV(border=False, ontop=True, aid="no", length=4)
#player.play('test.mp4')
player.play('rtsp://admin:false.memory@192.168.0.254/h264/ch1/main/av_stream')
player.wait_for_playback()
