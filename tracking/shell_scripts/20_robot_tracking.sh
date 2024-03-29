#!/bin/bash
export WORKON_HOME=/root/.virtualenvs
VIRTUALENVWRAPPER_PYTHON='/usr/bin/python'
. `which virtualenvwrapper.sh`
workon cv
for filename in real_experiments/videos/20_robots/*.MP4; do
    python tracking/tracking_scripts/kilobot_tracking.py -v $filename -n 20 -i 0
done
