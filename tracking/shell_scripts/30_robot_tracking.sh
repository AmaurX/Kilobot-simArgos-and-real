#!/bin/bash
export WORKON_HOME=/root/.virtualenvs
VIRTUALENVWRAPPER_PYTHON='/usr/bin/python'
. `which virtualenvwrapper.sh`
workon cv
for filename in videos/30_robots/*.MP4; do
python scripts/kilobot_tracking.py -v $filename -n 30 -i 0
done
