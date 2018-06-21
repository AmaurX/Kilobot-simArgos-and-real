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


def print_help():
    print("usage :  sim or real, [folders]")


def main():
    number_of_args = len(sys.argv)

    plt.figure(num=1, figsize=(15, 9), dpi=200, facecolor='w', edgecolor='k')

    if (number_of_args < 2):
        print_help()
        exit(-1)

    arena_size = "0.95"
    sim_or_real = sys.argv[1]

    folders = sys.argv[2:]

    if len(folders) == 1:
        interesting_folders = open(folders[0], 'rb')
        tsvin = csv.reader(interesting_folders, delimiter='\t')
        folders = []
        for row in tsvin:
            if(len(row) != 1):
                print("badly formatted interesting_folder file")
                exit(-1)
            else:
                folders.append(row[0])
                print(row[0])

    if(sim_or_real != "sim" and sim_or_real != "real"):
        print("ERROR: you must specify if this is sim or real as third argument")
        exit(-1)

    for folder in folders:
        total_num_robot = 0
        complete_time_dict = {}
        for directory, dirs, files in os.walk(folder):
            for element in files:
                if element.endswith('time_results.tsv'):
                    complete_time_dict, total_num_robot = first_discovery(
                        directory, element, total_num_robot, complete_time_dict, sim_or_real)
                else:
                    continue

        times = complete_time_dict.keys()
        times.append(0)
        times = sorted(times)
        values = [0]
        cummulate = 0
        linewidth = 3
        for key in times[1:]:
            cummulate += complete_time_dict[key]/total_num_robot
            values.append(cummulate)
        if(sim_or_real == "real" or "real_experiments" in folder):
            tick_per_second = 2
            linewidth = 5
            print(folder)
        else:
            tick_per_second = kilobot_ticks_per_second
        times = [float(i)/tick_per_second for i in times]
        legend = folder.strip("/").split('/')[-1]
        plt.plot(times, values, linewidth=linewidth, label=legend)
    plt.xlabel("Time in seconds")
    axes = plt.gca()
    axes.set_xlim([0.0, 1040])
    axes.set_ylim([0.0, 0.8])

    plt.ylabel("proportion of discovery")
    plt.title("Arena diameter: " + arena_size + "m ")
    plt.legend()
    plt.savefig("DiscoveryProportion_comparison.png",
                bbox_inches='tight', dpi=200, orientation="landscape")
    # plt.show(block=False)
    plt.close()


def first_discovery(folder, time_filename, total_number_of_robots, complete_time_dict, sim_or_real):
    complete_filename = folder + "/" + time_filename
    time_file = open(complete_filename, mode='rb')
    tsvin = csv.reader(time_file, delimiter='\t')
    num_robots = sum(1 for line in open(complete_filename)) - 1

    discovery_times = {}

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

                if(not discovery in complete_time_dict):
                    complete_time_dict[discovery] = 1.0
                else:
                    complete_time_dict[discovery] += 1.0

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

    return (complete_time_dict, total_number_of_robots)


if __name__ == '__main__':
    main()
