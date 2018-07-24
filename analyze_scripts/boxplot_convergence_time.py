import matplotlib.pyplot as plt
import numpy as np
import csv
import sys
import os
from scipy import stats
import math
from scipy.optimize import curve_fit
from scipy.stats import norm
import seaborn as sns
import pandas as pd

# Those must be the converted time results folders
real_file_folders = ["real_result_10_robots",
                     "real_result_20_robots", "real_result_30_robots"]
sim_file_folders = ["results_10_robots_cropped",
                    "results_20_robots_cropped", "results_30_robots_cropped"]


def main():
    total_dict = {'N': [], 'Convergence time': [], 'Type of experiment': []}
    for real_file_folder in real_file_folders:
        elements = real_file_folder.split("_")
        n = elements[2]  # Carefull as this can change
        proportion = 0
        total = 0
        convergence_times = []

        for filename in os.listdir(real_file_folder):
            with open(real_file_folder + "/" + filename, 'rb') as tsv_file:
                reader = csv.reader(tsv_file, delimiter=" ")
                for line in reader:
                    if(line[0] == "1"):
                        convergence_times.append(int(line[1]))
                total_dict['N'].extend(
                    [n]*len(convergence_times))
                total_dict['Convergence time'].extend(convergence_times)
                total_dict['Type of experiment'].extend(
                    ["real"]*len(convergence_times))

    for sim_file_folder in sim_file_folders:
        elements = sim_file_folder.split("_")
        n = elements[1]  # Carefull as this can change
        proportion = 0
        total = 0
        convergence_times = []
        for filename in os.listdir(sim_file_folder):
            if(filename.startswith("result_bias0.0_levy2.00_crw0.90_pop")):
                with open(sim_file_folder + "/" + filename, 'rb') as tsv_file:
                    reader = csv.reader(tsv_file, delimiter=" ")
                    for line in reader:
                        if(line[0] == "1"):
                            convergence_times.append(int(line[1]))
                    total_dict['N'].extend([n]*len(convergence_times))
                    total_dict['Convergence time'].extend(convergence_times)
                    total_dict['Type of experiment'].extend(
                        ["simulation"]*len(convergence_times))

    data_frame = pd.DataFrame.from_dict(total_dict)
    # frame = pd.DataFrame.from_dict(real_dict)
    print(data_frame)
    ax = sns.boxplot(x='N', y='Convergence time', hue='Type of experiment',
                     data=data_frame, palette="Set3")
    plt.show()


if __name__ == '__main__':
    main()
