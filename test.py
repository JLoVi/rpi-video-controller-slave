#!/usr/bin/env python3
import mpv
player = mpv.MPV( demuxer_thread="no", osc="no", border=False, fps="60", ontop=False, profile="low-latency", cache="no", untimed="yes", rtsp_transport="tcp", aid="no", input_vo_keyboard=True, brightness="0")
#player = mpv.MPV(border=False, ontop=True, aid="no", length=4)
#player.play('test.mp4')
player.play('rtsp://admin:false.memory@192.168.0.254/h265/ch1/main/av_stream')
player.wait_for_playback()
