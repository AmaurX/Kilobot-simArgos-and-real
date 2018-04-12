import matplotlib.pyplot as plt
import numpy as np
import csv
import sys
import os
from scipy import stats

number_of_args = len(sys.argv)
plt.figure(num=1, figsize=(12, 6), dpi=160, facecolor='w', edgecolor='k')


def print_help():
    print("usage : folder_path, number of robot per run, size of the arena")


def main():
    if (number_of_args < 4):
        print_help()
        exit(-1)

    folder = sys.argv[1]
    number_of_robots = int(sys.argv[2])
    arena_size = sys.argv[3]

    current_sum_displacement = []
    total_number_of_robots = 0
    displacement_run_count = 0
    for element in os.listdir(folder):
        if element.endswith('displacement.tsv'):
            displacement_run_count += 1
            (current_sum_displacement, total_number_of_robots, time_list) = displacement(folder, element, current_sum_displacement,
                                                                                         total_number_of_robots, number_of_robots)
        elif element.endswith('position.tsv'):
            continue
        elif element.endswith('time_results.tsv'):
            continue
        else:
            continue
    for i in range(len(current_sum_displacement)):
        current_sum_displacement[i] = current_sum_displacement[i] / \
            float(total_number_of_robots)

    slope, intercept, r_value, p_value, std_err = stats.linregress(
        time_list, current_sum_displacement)

    linear_approx = slope * time_list + intercept

    plt.plot(time_list, linear_approx, color='r', linewidth=2, linestyle=":",
             label="slope : " + "%.6f" % slope + " r^2 = " + "%.4f" % (r_value**2))
    plt.plot(time_list, current_sum_displacement, color='b', linewidth=3,
             label="MSD overtime on " + str(total_number_of_robots) + " robots")

    plt.xlabel("Time in ARGoS ticks")
    plt.ylabel("MSD in m^2")
    plt.title("Arena size: " + arena_size + "m*" +
              arena_size + "m, " + str(number_of_robots) + " kilobots per run, " + str(displacement_run_count) + " runs")
    plt.legend()
    plt.savefig(folder + "/MSD_"+arena_size + "m*" + arena_size +
                "m_" + str(number_of_robots) + "kilobots_" + str(displacement_run_count) + " runs.png", bbox_inches='tight', dpi=200, orientation="landscape")
    plt.show()


def displacement(folder, filename, current_sum_displacement, total_number_of_robots, num_robots):
    complete_filename = folder + "/" + filename
    displacement_file = open(complete_filename, mode='rb')
    tsvin = csv.reader(displacement_file, delimiter='\t')

    average_displacement = []
    time_list = []
    expe_length = 0

    for row in tsvin:
        if(row[0] == "Robot id"):
            average_displacement = np.zeros(len(row) - 2)
            expe_length = len(row) - 2
            time_list = np.zeros(len(row) - 2)
            for i in range(1, len(row) - 1):
                timestep = row[i].strip("t = ")
                timestep = timestep.strip('\t\n')
                timestep = float(timestep)
                time_list[i-1] = timestep
        else:
            for i in range(1, len(row)-1):
                average_displacement[i-1] += float(row[i])/num_robots

    if(len(current_sum_displacement) == 0):
        current_sum_displacement = np.zeros(expe_length)

    elif(len(current_sum_displacement) != expe_length):
        print("All experiments are not of the same length...")
        exit(-1)

    total_number_of_robots += num_robots
    for i in range(expe_length):
        current_sum_displacement[i] += float(num_robots) * \
            average_displacement[i]

    plt.plot(time_list, average_displacement,
             linewidth=0.5, linestyle='dashed')

    return (current_sum_displacement, total_number_of_robots, time_list)


main()
