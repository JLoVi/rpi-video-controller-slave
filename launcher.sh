#!/bin/sh
# launcher.sh
# navigate to home directory, then to this directory, then execute python script, then back home

cd /
cd home/pi/Projects/rpi-video-controller-slave #where the script is
sleep 20
python3 PlaybackController.py 4
#python3 PlaybackController.py $1 #a commnad to run the script
cd /
