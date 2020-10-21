#!/bin/sh
# launcher.sh
# navigate to home directory, then to this directory, then execute python script, then back home

export XDG_RUNTIME_DIR="/run/user/1000"
export DISPLAY=":0.0"
export XAUTHORITY="/home/pi/.Xauthority"
sleep 60
echo $XDG_RUNTIME_DIR
echo $DISPLAY
cd /
cd /home/pi/Projects/rpi-video-controller-slave
#python3 PlaybackController.py 4
#sudo XDG_RUNTIME_DIR="/run/user/1000"
python3 PlaybackController.py $1 1 &  #a commnad to run the script
