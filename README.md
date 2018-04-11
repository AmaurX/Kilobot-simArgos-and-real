# CLEAN KILOBOTS DIRECTORY / APRIL 2018

Created by Amaury Camus (amaury.camus92@gmail.com)     
Supervision : Vito Trianni

## Description
This is an attempt to create a self sufficient and clean repository for kilobots:

- For real robots
- For simulation on ARGoS

**TODO** verify dependancies (kilobot libs, argos3 libs etc...) --> may require installations in /usr/include and /usr/lib.

## src folder
It contains all the code. See internal README for more information  

## Build and use

### Building
At the root folder (same level as src):  
`mkdir build` (if it doesn't already exists)    
`cd build`   
`cmake ../src`   
`make`   
`sudo -H make install` To install the kilobot argos3 libs and headers    

It should compile everything.     
- The binary files needed for simulations in ARGoS are in build/behaviors_simulation
- The .hex files needed for real kilobots are in build/behaviors_real

**TODO** : install step : create a install folder, that would only contain dynamic libs and the above files.

### Launching a simulation
Steps:
- Make sure you have argos3 installed (typing `which argos3` should give the path to the executable)  
- Make sure you are in the root folder
- From the root folder, use the command `argos3 -c simulation_config/MY_CONFIG.argos`

