# src folder

## Behaviors folder
The behaviors (native kilobot code) should work the same exact way for
both real and simulation.   
In the folder is also a **CMakeLists.txt** that is only to compile the behaviors for **ARGoS**. It should be, if possible, move somewhere named explicitely with simulation.   
The goal of this folder is to contain the behaviors and only the behaviors.

## cmake folder
This folder is used to set cmake to compile for ARGoS   

## kilobots folder
This folder contains the code to compile behaviors for real robots.    
The Makefile contains the real compilation instructions, but to make it easy to build everything, there is a CMakelist.txt that just calls the makefile.

The content of this folder **shoud not be modified** except for the Makefile, to add compilation of new behaviors.    

**Warning** The Makefile isn't very well designed, and is very project-architecture dependent, meaning that if you move things around, you might have to change paths inside it if you don't want to break it.   

## plugins folder
This folder contains the code which creates the library that is used to compile behaviors for simulation.    
**It should not be modified**.    
__Warning__ : I did modify it a bit, adding loop functions (ci_kilobot_loop_functions) into the library, but as they are custom for one specific purpose, they should be placed in another folder. For now, it poses problem with the make process (right now, it is easier to compile with the rest of the kilobot plugin library).


## CMakelists.txt
This CMakelists.txt initializes variables and calls the compilation of:
- The argos-kilobot plugin
- The behaviors for compilation
- The behaviors for real kilobots (with the Makefile as seen previously)

Normaly, it should not be modified, except if you have to add include or library paths. Be advised, adding include path and lib path in the Cmakes will not put them in the scope of the Makefile (in the makefile, path are also added when needed). There might be a better and more elegant solution.
