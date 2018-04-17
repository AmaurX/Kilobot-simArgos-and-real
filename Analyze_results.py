import matplotlib.pyplot as plt
import numpy as np
import csv
import sys
import os
from scipy import stats

number_of_args = len(sys.argv)
plt.figure(num=1, figsize=(12, 6), dpi=160, facecolor='w', edgecolor='k')
plt.figure(num=2, figsize=(12, 6), dpi=160, facecolor='w', edgecolor='k')


def print_help():
    print("usage : folder_path, number of robot per run, size of the arena, window size (for windowed_MSD)")


def main():
    if (number_of_args < 5):
        print_help()
        exit(-1)

    folder = sys.argv[1]
    number_of_robots = int(sys.argv[2])
    arena_size = sys.argv[3]
    window_size = int(sys.argv[4])

    current_sum_displacement = []
    total_number_of_robots = 0
    displacement_run_count = 0

    for element in os.listdir(folder):
        if element.endswith('displacement.tsv'):
            displacement_run_count += 1
            (current_sum_displacement, total_number_of_robots, time_list) = displacement(folder, element, current_sum_displacement,
                                                                                         total_number_of_robots, number_of_robots)
        else:
            continue
    for i in range(len(current_sum_displacement)):
        current_sum_displacement[i] = current_sum_displacement[i] / \
            float(total_number_of_robots)

    time_list = time_list[:len(current_sum_displacement)]
    slope, intercept, r_value, p_value, std_err = stats.linregress(
        time_list, current_sum_displacement)

    linear_approx = slope * time_list + intercept

    plt.plot(time_list, linear_approx, color='r', linewidth=2, linestyle=":",
             label="slope : " + "%.4e" % slope + " r^2 = " + "%.4f" % (r_value**2))
    plt.plot(time_list, current_sum_displacement, color='b', linewidth=3,
             label="MSD overtime on " + str(total_number_of_robots) + " robots")

    plt.xlabel("Time in ARGoS ticks")
    plt.ylabel("MSD in m^2")
    plt.title("Arena diameter: " + arena_size + "m "
              + str(number_of_robots) + " kilobots per run, " + str(displacement_run_count) + " runs")
    plt.legend()
    plt.savefig(folder + "/MSD_"+arena_size + "m*" + arena_size +
                "m_" + str(number_of_robots) + "kilobots_" + str(displacement_run_count) + " runs.png", bbox_inches='tight', dpi=200, orientation="landscape")
    # plt.show(block=False)
    plt.close()

    current_sum_w_displacement = []
    w_total_number_of_robots = 0
    w_displacement_run_count = 0
    time_period = 0
    for element in os.listdir(folder):
        if element.endswith('position.tsv'):
            w_displacement_run_count += 1
            (current_sum_w_displacement, w_total_number_of_robots, time_list, time_period) = window_displacement(folder, element, current_sum_w_displacement,
                                                                                                                 w_total_number_of_robots, number_of_robots, window_size)
        else:
            continue

    for i in range(len(current_sum_w_displacement)):
        current_sum_w_displacement[i] = current_sum_w_displacement[i] / \
            float(w_total_number_of_robots)
    time_list = time_list[:len(current_sum_w_displacement)]

    slope, intercept, r_value, p_value, std_err = stats.linregress(
        time_list, current_sum_w_displacement)

    linear_approx = slope * time_list + intercept
    plt.plot(time_list, linear_approx, color='r', linewidth=2, linestyle=":",
             label="slope : " + "%.4e" % slope + " r^2 = " + "%.4f" % (r_value**2))
    plt.plot(time_list, current_sum_w_displacement, color='b', linewidth=3,
             label="Window MSD (window = " + str(time_period * window_size) + " ticks) overtime on " + str(w_total_number_of_robots) + " robots")

    plt.xlabel("Time in ARGoS ticks")
    plt.ylabel("MSD in m^2")
    plt.title("Arena diameter: " + arena_size + "m " +
              str(number_of_robots) + " kilobots per run, " + str(w_displacement_run_count) + " runs")
    plt.legend()
    plt.savefig(folder + "/Window_MSD_"+arena_size + "m*" + arena_size +
                "m_" + str(number_of_robots) + "kilobots_" + str(w_displacement_run_count) + " runs.png", bbox_inches='tight', dpi=200, orientation="landscape")
    # plt.show(block=False)
    plt.close()


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

    elif(len(current_sum_displacement) > expe_length):
        current_sum_displacement = current_sum_displacement[:expe_length]
        time_list = time_list[:expe_length]
        print("All experiments are not of the same length...")
    elif(len(current_sum_displacement) < expe_length):
        expe_length = len(current_sum_displacement)

    total_number_of_robots += num_robots
    for i in range(expe_length):
        current_sum_displacement[i] += float(num_robots) * \
            average_displacement[i]

    plt.plot(time_list, average_displacement,
             linewidth=0.5, linestyle='dashed')

    return (current_sum_displacement, total_number_of_robots, time_list)


def window_displacement(folder, position_filename, current_sum_w_displacement, total_number_of_robots, num_robots, window_size):
    complete_filename = folder + "/" + position_filename
    displacement_file = open(complete_filename, mode='rb')
    tsvin = csv.reader(displacement_file, delimiter='\t')

    average_w_displacement = []
    time_list = []
    expe_length = 0
    time_period = 0

    for row in tsvin:
        if(row[0] == "Robot id"):
            expe_length = len(row) - 2 - window_size

            average_w_displacement = np.zeros(expe_length)
            time_list = np.zeros(expe_length)
            time_period = int(row[2].strip("t = ").strip('\t\n'))

            for i in range(1 + window_size, len(row) - 1):
                timestep = row[i].strip("t = ")
                timestep = timestep.strip('\t\n')
                timestep = float(timestep)
                time_list[i-1 - window_size] = timestep
        else:
            # for i in range(1, window_size + 1):
            #     [xi, yi] = row[1].split(",")
            #     [xi, yi] = [float(xi), float(yi)]

            #     [xf, yf] = row[i].split(",")
            #     [xf, yf] = [float(xf), float(yf)]

            #     w_displacement = (xf - xi)**2 + (yf - yi)**2
            #     w_displacement /= num_robots

            #     average_w_displacement[i-1] += w_displacement
            for i in range(1 + window_size, len(row)-1):
                [xi, yi] = row[i-window_size].split(",")
                [xi, yi] = [float(xi), float(yi)]

                [xf, yf] = row[i].split(",")
                [xf, yf] = [float(xf), float(yf)]

                w_displacement = ((xf - xi)/window_size)**2 + \
                    ((yf - yi)/window_size)**2
                w_displacement /= num_robots

                average_w_displacement[i-1 - window_size] += w_displacement

    if(len(current_sum_w_displacement) == 0):
        current_sum_w_displacement = np.zeros(expe_length)

    elif(len(current_sum_w_displacement) > expe_length):
        current_sum_w_displacement = current_sum_w_displacement[:expe_length]
        time_list = time_list[:expe_length]
        print("All experiments are not of the same length...")
    elif(len(current_sum_w_displacement) < expe_length):
        expe_length = len(current_sum_w_displacement)

    total_number_of_robots += num_robots
    for i in range(expe_length):
        current_sum_w_displacement[i] += float(num_robots) * \
            average_w_displacement[i]

    plt.plot(time_list, average_w_displacement,
             linewidth=0.5, linestyle='dashed')

    return (current_sum_w_displacement, total_number_of_robots, time_list, time_period)


main()
