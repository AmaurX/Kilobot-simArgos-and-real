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

# default value
kilobot_ticks_per_second = 31


def print_help():
    print("usage : folder_path, sim or real ,window size (for windowed_MSD)")


def main():
    number_of_args = len(sys.argv)

    if (number_of_args < 4):
        print_help()
        exit(-1)

    folder = sys.argv[1]
    sim_or_real = sys.argv[2]
    window_size = int(sys.argv[3]) * 2

    if(sim_or_real != "sim" and sim_or_real != "real"):
        print("ERROR: you must specify if this is sim or real as third argument")
        exit(-1)

    total_dict = dict()
    number_dict = dict()

    for directory, dirs, files in os.walk(folder):
        n = "0"
        rho = -1.0
        alpha = -1.0
        elements = directory.split("_")
        print(directory)
        for e in elements:
            if e.startswith("robots"):
                n = e.split("=")[-1]
                if(not total_dict.has_key(n)):
                    total_dict[n] = dict()
                    number_dict[n] = dict()

            if(e.startswith("rho")):
                rho = float(e.split("=")[-1])
            if(e.startswith("alpha")):
                alpha = float(e.split("=")[-1])
        if(n == "0" or rho == -1.0 or alpha == -1.0):
            print("THERE WAS A PROBLEM IN THE NAME OF THE FOLDER, GOING TO THE NEXT")
            continue
        rho_str = str(rho)
        alpha_str = str(alpha)
        if(not total_dict[n].has_key(rho_str)):
            total_dict[n][rho_str] = dict()
            number_dict[n][rho_str] = dict()
        mean_wmsd = 0.0
        number_of_experiments = 0
        for one_file in files:
            if one_file.endswith('position.tsv'):
                (mean_wmsd, number_of_experiments) = window_displacement(
                    os.path.join(directory, one_file), mean_wmsd, number_of_experiments, window_size, int(n))

        if(number_dict[n][rho_str].has_key(alpha_str)):
            previous_number = number_dict[n][rho_str][alpha_str]
            total_dict[n][rho_str][alpha_str] *= previous_number
            total_dict[n][rho_str][alpha_str] += mean_wmsd * \
                number_of_experiments
            total_dict[n][rho_str][alpha_str] /= previous_number + \
                number_of_experiments
            number_dict[n][rho_str][alpha_str] += number_of_experiments
        else:
            total_dict[n][rho_str][alpha_str] = mean_wmsd
            number_dict[n][rho_str][alpha_str] = number_of_experiments

    print(total_dict)
    for key, value in total_dict.iteritems():
        fig = plt.figure(figsize=(12, 8))
        dataFrame = pd.DataFrame.from_dict(value)
        reversed_df = dataFrame.iloc[::-1]
        ax = sns.heatmap(reversed_df, annot=True, fmt=".2e")
        ax.set_title("Heatmap of WMSD for %s robots" % (key))
        ax.set_ylabel("alpha")
        ax.set_xlabel("rho")
        plt.savefig("%s/WMSD_%s_robots_heatmap.png" % (folder, key))
    # for i in range(len(current_sum_w_displacement)):
    #     current_sum_w_displacement[i] = current_sum_w_displacement[i] / \
    #         float(w_total_number_of_robots)
    # time_list = time_list[:len(current_sum_w_displacement)]

    # slope, intercept, r_value, p_value, std_err = stats.linregress(
    #     time_list, current_sum_w_displacement)

    # linear_approx = [slope * i + intercept for i in time_list]
    # plt.plot(time_list, linear_approx, color='r', linewidth=2, linestyle=":",
    #          label="slope : " + "%.4e" % slope + " r^2 = " + "%.4f" % (r_value**2))
    # plt.plot(time_list, current_sum_w_displacement, color='b', linewidth=3,
    #          label="Window MSD (window = " + str(window_size/2) + " seconds) overtime on " + str(w_total_number_of_robots) + " robots")

    # plt.xlabel("Time in seconds")
    # plt.ylabel("MSD in m^2")
    # plt.title("Arena diameter: " + arena_size + "m " +
    #           str(number_of_robots) + " kilobots per run, " + str(w_displacement_run_count) + " runs")
    # plt.legend()
    # plt.savefig(folder + "/Window_MSD_" + str(number_of_robots) + "kilobots_" +
    #             str(w_displacement_run_count) + " runs.png", bbox_inches='tight', dpi=200, orientation="landscape")
    # # plt.show(block=False)
    # plt.close()


def window_displacement(position_filename, mean_wmsd, number_of_experiments, window_size, num_robots):
    displacement_file = open(position_filename, mode='rb')
    tsvin = csv.reader(displacement_file, delimiter='\t')

    average_w_displacement = []
    time_list = []
    expe_length = 0
    time_period = 0

    for row in tsvin:
        if(row[0] == "Robot id"):
            expe_length = len(row) - 1 - 2 * window_size

            average_w_displacement = np.zeros(expe_length)
        else:
            # for i in range(1, window_size + 1):
            #     [xi, yi] = row[1].split(",")
            #     [xi, yi] = [float(xi), float(yi)]

            #     [xf, yf] = row[i].split(",")
            #     [xf, yf] = [float(xf), float(yf)]

            #     w_displacement = (xf - xi)**2 + (yf - yi)**2
            #     w_displacement /= num_robots

            #     average_w_displacement[i-1] += w_displacement
            for i in range(1 + window_size, len(row)-window_size):
                [xi, yi] = row[i-window_size].split(",")
                [xi, yi] = [float(xi), float(yi)]

                [xf, yf] = row[i].split(",")
                [xf, yf] = [float(xf), float(yf)]

                w_displacement = ((xf - xi)/window_size*2)**2 + \
                    ((yf - yi)/window_size*2)**2
                w_displacement /= num_robots

                average_w_displacement[i-1 - window_size] += w_displacement
    number_of_value = len(average_w_displacement)
    mean = 0.0
    for i in average_w_displacement:
        mean = mean + i/number_of_value

    if(number_of_experiments == 0):
        mean_wmsd = mean
        number_of_experiments += 1
    else:
        mean_wmsd *= number_of_experiments
        mean_wmsd += mean
        number_of_experiments += 1
        mean_wmsd /= float(number_of_experiments)

    return (mean_wmsd, number_of_experiments)


if __name__ == '__main__':
    main()
