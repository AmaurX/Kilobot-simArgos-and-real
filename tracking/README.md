# Kilobot tracking repository
Created by Amaury Camus (may 2018)

## Description

This is a custom kilobot tracking algorithm that adapts to a overhead camera on our circular arena.

The currently functionning script is kilobot_tracking.py
It uses template matching. The templates are in kilobot_templates and target_templates.

ball_tracking.py is an attempt at blob detection, by color filtering, but doesnt seem to give good results
ball_tracking_3.py is an attempt at using feature detection. It seems the kilobot is to simple to have enough interesting features to recognize...