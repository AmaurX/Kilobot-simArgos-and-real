# Kilobot tracking repository
Created by Amaury Camus (may 2018)

## Description

This is a custom kilobot tracking algorithm that adapts to a overhead camera on our circular arena.

The currently functionning script is **tracking_script/kilobot_tracking.py**

# Python scripts in tracking_script folder

**PRE-REQUISITE**  
You will need an installation of openCV (with python 2.7 or 3.5, but this was done with 2.7 so there might be changes to make to the code if you use python 3.5 or after).   
**My advice** is to follow exactly [this procedure](https://www.pyimagesearch.com/2016/10/24/ubuntu-16-04-how-to-install-opencv/), even concerning the python virtual environment. It will save you a lot of trouble.

## kilobot&#46;py
This is the Kilobot class module used to represent and log kilobot state. It is used by kilobot_tracking.py and should not be changed

## kilobot_tracking.py
_**This is the main tracking scripts**_, that uses the Kilobot class (see before). It contains all the differents adjustment variables to make the tracing work :
- definition of colors
- definition of threshold values for pattern matching detection
- definition of the size and location of the arena (as it can change, you will also use the find_starting_frame.py (see below))
- definition of the conversion factor meter/pixel (that can change if the camera is at a different emplacememt)
- definition of kilobot properties (radius, max comm range, max speed etc...)

**If you wish to use this tracking algorithm, here are my recommandations:**
- On several images of your experiments, re-extract kilobot templates as thoses present in the template folder
- With the range_detector.py script (see below), re-define all color values (that are used to exclude false positives on detection and to find led colors)
- re-define the conversion meter/pixel and all other pixel values  

Then, just run it with associated arguments :   
`python kilobot_tracking.py -v /path/to/video.MP4 -n $number_of_robots`   
See the file help for additional arguments (vizualisation etc...)

## find_starting_frame.py
As you will not always start the experiment at the first frame of the video, this script will allow you to find the first frame of each video, and also to rectify the position and size of the arena automatically. It will then write a small text file that will be read first by the tracking_kilobot.py script.
To use it, just type 
- `python find_starting_frame.py -v $video`   to do it on a single video
- `python find_starting_frame.py -f $folder`   to do it on all videos in $folder

## range_detector.py
Give a screenshot of your experiment to this script, with the command `python range-detector.py --filter RGB --image /path/to/image.png` and then play with the values to identify the 6 values that define a range of wanted color.
I identified 4 colors:
- The grey color of the table, to exclude all pattern detection that has too much grey (and is thus a false positive)
- The bright green and purple colors of the led
- The dark green color of the target support (to also avoid false positives next to the target)

With a change of camera and experiment environment, these will completely change.

## camera_fr_check.py
Just a small script to show the first and last image of a video which films a chronometer, to calculate accuractly the frequency of the camera. For information, the frequency of the Gopro was **very** accurate at 2Hz.

# Shell scripts
This folder just contains examples of the scripts used to launch the tracking on the cluster.