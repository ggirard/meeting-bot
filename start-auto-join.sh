#！/bin/bash 
xhost +local:root
export DISPLAY=:0.0
python auto-join.py
