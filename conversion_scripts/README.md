# Description
This is a module to convert time data obtained from experiments by ARGoS or the tracking scripts.    
It will take time data from the experiments and produce for each set of parameters alpha and rho a file corresponding to the plotting tool provided by Aishwarya Unnikrishnan. 

In short, just run the convert_all_data.py script with arguments:
- the overall folder of the experiments
- 'sim' or 'real'
- optionnal : a time, in second, at whoch to crop time results (for instance to have same length between real and simulated experiments) 

You can also run the simple convert_data.py, that will take just one specific experiment folder. It is not advised as it will just convert part of the data.

