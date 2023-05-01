#!/bin/sh

# systray battery icon
cbatticon -u 5 &
# systray volume
volumeicon &
feh --bg-fill -r -z ~/Desktop/castv/wallpapers
picom --no-vsync &
~/.config/polybar/launch.sh $