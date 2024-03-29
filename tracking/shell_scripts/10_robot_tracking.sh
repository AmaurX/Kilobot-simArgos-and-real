#!/bin/bash
export WORKON_HOME=/root/.virtualenvs
VIRTUALENVWRAPPER_PYTHON='/usr/bin/python'
. `which virtualenvwrapper.sh`
workon cv
for filename in real_experiments/videos/10_robots/*.MP4; do
    python tracking/tracking_scripts/kilobot_tracking.py -v $filename -n 10 -i 0
done
