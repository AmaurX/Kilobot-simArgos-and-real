# CLEAN KILOBOTS DIRECTORY / APRIL 2018

Created by Amaury Camus (amaury.camus92@gmail.com)     
Supervision : Vito Trianni

## Description
This is an attempt to create a self sufficient and clean repository for kilobots:

- For real robots
- For simulation on ARGoS

## src folder
It contains all the code. See internal README for more information  

## Build and use

### Dependancies
Prior to using this work, you should have installed:

- Argos3 (from sources : https://github.com/ilpincy/argos3 , installed in usr/local)
- Argos3 kilobot plugin (from sources : https://github.com/ilpincy/argos3-kilobot , installed in usr/local)

The current state of this works allows me to make it work on ubuntu 16.04 and 14.04, though I don't know for mac OS.

### Building
At the root folder (same level as src):  
`mkdir build` (if it doesn't already exists)    
`cd build`   
`cmake ../src`   
`make`   

It should compile everything.     
- Thanks to the cmakelists.txt in behaviors, with its for loops, you can specify the whole range of parameters for which you want to run experiments. Is should generate:  
     - The binary behavior files in build/behaviors_simulation
     - The config files in simulation_config/generated_configs
- The .hex files needed for real kilobots are in build/behaviors_real

**TODO** : install step : create a install folder, that would only contain dynamic libs and the above files.

### Launching a simulation
Steps:
- Make sure you have argos3 installed (typing `which argos3` should give the path to the executable)  
- Make sure you are in the root folder
- From the root folder, use the command `argos3 -c simulation_config/MY_CONFIG.argos`

