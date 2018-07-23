import matplotlib.pyplot as plt
import numpy as np
import csv
import sys
import os
from scipy import stats
import math
from scipy.optimize import curve_fit
from scipy.stats import norm


# default value
kilobot_ticks_per_second = 31

colors = {"10": 'm',
          "20": 'c',
          "30": 'y',
          "all": 'b'}


def print_help():
    print(
        "usage :  sim or real, [folders or text file containing the list of experiment folders]")


def main():
    number_of_args = len(sys.argv)

    plt.figure(num=1, figsize=(10, 6), dpi=200, facecolor='w', edgecolor='k')

    if (number_of_args < 2):
        print_help()
        exit(-1)

    sim_or_real = sys.argv[1]

    folders = sys.argv[2:]

    if len(folders) == 1:
        interesting_folders = open(folders[0], 'rb')
        tsvin = csv.reader(interesting_folders, delimiter='\t')
        folders = []
        for row in tsvin:
            if(len(row) != 1):
                print("badly formatted interesting_folders file")
                exit(-1)
            else:
                folders.append(row[0])
                print(row[0])

    if(sim_or_real != "sim" and sim_or_real != "real"):
        print("ERROR: you must specify if this is sim or real as first argument. \n \
              If the folder contains the string 'real_experiments' it will be considered as a real experiment een if the rest is sim.")
        exit(-1)

    for folder in folders:
        total_num_robot = 0
        complete_time_dict = {}
        n_robots = {}
        for directory, _, files in os.walk(folder):
            for element in files:
                if element.endswith('time_results.tsv'):
                    complete_time_dict, total_num_robot, n_robots = first_discovery(
                        directory, element, total_num_robot, complete_time_dict, n_robots, sim_or_real)
                else:
                    continue
        for n, value in complete_time_dict.iteritems():
            if(n == "all"):
                times = value.keys()
                times.append(0)
                times = sorted(times)
                values = [0]
                cummulate = 0
                linewidth = 4
                linestyle = ':'
                for key in times[1:]:
                    cummulate += value[key]/total_num_robot
                    values.append(cummulate)
                if(sim_or_real == "real" or "real_experiments" in folder):
                    tick_per_second = 2
                    linestyle = '-'
                    print(folder)
                else:
                    tick_per_second = kilobot_ticks_per_second
                times = [float(i)/tick_per_second for i in times]
                legend = (folder.strip("/").split('/')
                          [-1]).split("_")[0] + " " + (folder.strip("/").split('/')
                                                       [-1]).split("_")[1] + " " + n + " robots"
                # if(n == "all"):
                plt.plot(times, values, linestyle + colors[n],
                         linewidth=linewidth, label=legend)
            else:
                times = value.keys()
                times.append(0)
                times = sorted(times)
                values = [0]
                cummulate = 0
                linewidth = 1
                for key in times[1:]:
                    cummulate += value[key]/n_robots[n]
                    values.append(cummulate)
                linestyle = ':'
                if(sim_or_real == "real" or "real_experiments" in folder):
                    tick_per_second = 2
                    linestyle = '-'
                    print(folder)
                else:
                    tick_per_second = kilobot_ticks_per_second
                times = [float(i)/tick_per_second for i in times]
                legend = (folder.strip("/").split('/')
                          [-1]).split("_")[0] + " " + (folder.strip("/").split('/')
                                                       [-1]).split("_")[1] + " " + n + " robots"
                # if(n == "all"):
                plt.plot(times, values, linestyle + colors[n],
                         linewidth=linewidth, label=legend)
    plt.xlabel("Time in seconds")
    axes = plt.gca()
    axes.set_xlim([0.0, 600])
    axes.set_ylim([0.0, 0.6])
    handles, labels = plt.gca().get_legend_handles_labels()

    order = [1, 5, 0, 4, 3, 7, 2, 6]
    plt.legend([handles[idx] for idx in order], [labels[idx] for idx in order])
    # plt.legend()
    plt.ylabel("proportion of discovery")
    plt.title("First passage time distribution")
    plt.savefig("DiscoveryProportion_comparison.png",
                bbox_inches='tight', dpi=200, orientation="landscape")
    # plt.show(block=False)
    plt.close()


def first_discovery(folder, time_filename, total_number_of_robots, complete_time_dict, n_robots, sim_or_real):
    complete_filename = folder + "/" + time_filename
    time_file = open(complete_filename, mode='rb')
    tsvin = csv.reader(time_file, delimiter='\t')
    num_robots = sum(1 for line in open(complete_filename)) - 1

    discovery_times = {}
    n = "0"
    elements = folder.split("_")
    for e in elements:
        if(e.startswith("robots")):
            n = e.split("=")[-1]
    if(not complete_time_dict.has_key(n)):
        complete_time_dict[n] = dict()
        n_robots[n] = 0
    if(not complete_time_dict.has_key("all")):
        complete_time_dict["all"] = dict()
    for row in tsvin:
        if(row[0] == "Robot id"):
            continue
        else:
            if(len(row) < 3):
                print(complete_filename)
            discovery = int(row[1])
            if(discovery > 0):
                if(not discovery in discovery_times):
                    discovery_times[discovery] = 1.0/num_robots
                else:
                    discovery_times[discovery] += 1.0/num_robots

                if(not discovery in complete_time_dict[n]):
                    complete_time_dict[n][discovery] = 1.0
                else:
                    complete_time_dict[n][discovery] += 1.0

                if(not discovery in complete_time_dict["all"]):
                    complete_time_dict["all"][discovery] = 1.0
                else:
                    complete_time_dict["all"][discovery] += 1.0

    times = discovery_times.keys()
    times.append(0)
    times = sorted(times)
    values = [0]
    cummulate = 0
    for key in times[1:]:
        cummulate += discovery_times[key]
        values.append(cummulate)

    if(sim_or_real == "real" or "real_expirements" in folder):
        tick_per_second = 2
        # print(folder)

    else:
        tick_per_second = kilobot_ticks_per_second

    times = [float(i)/tick_per_second for i in times]
    # plt.plot(times, values, linewidth=0.5, linestyle='dashed')
    total_number_of_robots += num_robots
    n_robots[n] += num_robots

    return (complete_time_dict, total_number_of_robots, n_robots)


if __name__ == '__main__':
    main()
