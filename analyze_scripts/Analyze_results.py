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
    print("usage : folder_path, number of robot per run, sim or real ,window size (for windowed_MSD), argos ticks per second")


def main():
    number_of_args = len(sys.argv)

    plt.figure(num=1, figsize=(12, 6), dpi=160, facecolor='w', edgecolor='k')
    plt.figure(num=2, figsize=(12, 6), dpi=160, facecolor='w', edgecolor='k')
    plt.figure(num=3, figsize=(12, 6), dpi=160, facecolor='w', edgecolor='k')
    plt.figure(num=4, figsize=(12, 6), dpi=160, facecolor='w', edgecolor='k')
    plt.figure(num=5, figsize=(12, 6), dpi=160, facecolor='w', edgecolor='k')

    if (number_of_args < 5):
        print_help()
        exit(-1)

    folder = sys.argv[1]
    number_of_robots = int(sys.argv[2])
    arena_size = "0.95"
    sim_or_real = sys.argv[3]
    window_size = int(sys.argv[4]) * 2
    argos_ticks_per_second = int(sys.argv[5])
    current_sum_displacement = []
    total_number_of_robots = 0
    displacement_run_count = 0

    if(sim_or_real != "sim" and sim_or_real != "real"):
        print("ERROR: you must specify if this is sim or real as third argument")
        exit(-1)

    time_list = []

    for directory, dirs, files in os.walk(folder):
        for element in files:
            if element.endswith('displacement.tsv'):
                displacement_run_count += 1
                (current_sum_displacement, total_number_of_robots, time_list) = displacement(directory, element, current_sum_displacement,
                                                                                             total_number_of_robots, number_of_robots, argos_ticks_per_second)
            else:
                continue
    for i in range(len(current_sum_displacement)):
        current_sum_displacement[i] = current_sum_displacement[i] / \
            float(total_number_of_robots)

    time_list = time_list[:len(current_sum_displacement)]
    slope, intercept, r_value, p_value, std_err = stats.linregress(
        time_list, current_sum_displacement)

    linear_approx = [slope * i + intercept for i in time_list]

    plt.plot(time_list, linear_approx, color='r', linewidth=2, linestyle=":",
             label="slope : " + "%.4e" % slope + " r^2 = " + "%.4f" % (r_value**2))
    plt.plot(time_list, current_sum_displacement, color='b', linewidth=3,
             label="MSD overtime on " + str(total_number_of_robots) + " robots")

    plt.xlabel("Time in seconds")
    plt.ylabel("MSD in m^2")
    plt.title("Arena diameter: " + arena_size + "m "
              + str(number_of_robots) + " kilobots per run, " + str(displacement_run_count) + " runs")
    plt.legend()
    plt.savefig(folder + "/MSD_" + str(number_of_robots) + "kilobots_" + str(displacement_run_count) +
                " runs.png", bbox_inches='tight', dpi=200, orientation="landscape")
    # plt.show(block=False)
    plt.close()

    current_sum_w_displacement = []
    w_total_number_of_robots = 0
    w_displacement_run_count = 0
    time_period = 0
    for directory, dirs, files in os.walk(folder):
        for element in files:
            if element.endswith('position.tsv'):
                w_displacement_run_count += 1
                (current_sum_w_displacement, w_total_number_of_robots, time_list, time_period) = window_displacement(directory, element, current_sum_w_displacement,
                                                                                                                     w_total_number_of_robots, number_of_robots, window_size, argos_ticks_per_second, sim_or_real)
            else:
                continue

    for i in range(len(current_sum_w_displacement)):
        current_sum_w_displacement[i] = current_sum_w_displacement[i] / \
            float(w_total_number_of_robots)
    time_list = time_list[:len(current_sum_w_displacement)]

    slope, intercept, r_value, p_value, std_err = stats.linregress(
        time_list, current_sum_w_displacement)

    linear_approx = [slope * i + intercept for i in time_list]
    plt.plot(time_list, linear_approx, color='r', linewidth=2, linestyle=":",
             label="slope : " + "%.4e" % slope + " r^2 = " + "%.4f" % (r_value**2))
    plt.plot(time_list, current_sum_w_displacement, color='b', linewidth=3,
             label="Window MSD (window = " + str(window_size/2) + " seconds) overtime on " + str(w_total_number_of_robots) + " robots")

    plt.xlabel("Time in seconds")
    plt.ylabel("MSD in m^2")
    plt.title("Arena diameter: " + arena_size + "m " +
              str(number_of_robots) + " kilobots per run, " + str(w_displacement_run_count) + " runs")
    plt.legend()
    plt.savefig(folder + "/Window_MSD_" + str(number_of_robots) + "kilobots_" +
                str(w_displacement_run_count) + " runs.png", bbox_inches='tight', dpi=200, orientation="landscape")
    # plt.show(block=False)
    plt.close()

    if(sim_or_real == "real"):
        tick_per_second = 2
    else:
        tick_per_second = kilobot_ticks_per_second
    total_num_robot = 0
    complete_time_dict = {}
    for directory, dirs, files in os.walk(folder):
        for element in files:
            if element.endswith('time_results.tsv'):
                complete_time_dict, total_num_robot = first_discovery(
                    directory, element, number_of_robots, total_num_robot, complete_time_dict, sim_or_real)
            else:
                continue

    times = complete_time_dict.keys()
    times.append(0)
    times = sorted(times)
    values = [0]
    cummulate = 0
    for key in times[1:]:
        cummulate += complete_time_dict[key]/total_num_robot
        values.append(cummulate)
    times = [float(i)/tick_per_second for i in times]

    plt.plot(times, values, linewidth=3, color='b')
    plt.xlabel("Time in seconds")
    plt.ylabel("proportion of discovery")
    plt.title("Arena diameter: " + arena_size + "m " +
              str(number_of_robots) + " kilobots per run, " + str(w_displacement_run_count) + " runs")
    plt.legend()
    plt.savefig(folder + "/DiscoveryProportion_" + str(number_of_robots) + "kilobots_" +
                str(w_displacement_run_count) + " runs.png", bbox_inches='tight', dpi=200, orientation="landscape")
    # plt.show(block=False)
    plt.close()

    total_num_robot = 0
    complete_time_dict = {}
    for directory, dirs, files in os.walk(folder):
        for element in files:
            if element.endswith('time_results.tsv'):
                complete_time_dict, total_num_robot = first_information(
                    directory, element, number_of_robots, total_num_robot, complete_time_dict, sim_or_real)
            else:
                continue

    times = complete_time_dict.keys()
    times.append(0)
    times = sorted(times)
    values = [0]
    cummulate = 0
    for key in times[1:]:
        cummulate += complete_time_dict[key]/total_num_robot
        values.append(cummulate)

    times = [float(i)/tick_per_second for i in times]

    plt.plot(times, values, linewidth=3, color='b')
    plt.xlabel("Time in seconds")
    plt.ylabel("proportion of information")
    plt.title("Arena diameter: " + arena_size + "m " +
              str(number_of_robots) + " kilobots per run, " + str(w_displacement_run_count) + " runs")
    plt.legend()
    plt.savefig(folder + "/informationProportion_" + str(number_of_robots) + "kilobots_" +
                str(w_displacement_run_count) + " runs.png", bbox_inches='tight', dpi=200, orientation="landscape")
    # plt.show(block=False)
    plt.close()

    ##########################################################
    n = 1
    if(sim_or_real == "real"):
        n = 2
    n_sec_distance_list = []
    total_number_of_robots = 0
    w_displacement_run_count = 0
    for directory, dirs, files in os.walk(folder):
        for element in files:
            if element.endswith('position.tsv'):
                w_displacement_run_count += 1
                (n_sec_distance_list, total_number_of_robots) = n_sec_dist(directory, element,
                                                                           n_sec_distance_list, n, total_number_of_robots, number_of_robots, argos_ticks_per_second, sim_or_real)

            else:
                continue

    n2, bins, _ = plt.hist(n_sec_distance_list, bins='auto', density=1)
    centers = (0.5*(bins[1:]+bins[:-1]))
    pars, cov = curve_fit(lambda total_list, mu, sig: norm.pdf(
        total_list, loc=mu, scale=sig), centers, n2, p0=[0, 1])
    # axes = plt.gca()
    # axes.set_xlim([0.0, 0.025])

    def gauss(x, mu, sigma, A):
        return A*np.exp(-(x-mu)**2/2/sigma**2)

    def bimodal_gauss(x, mu1, sigma1, A1, mu2, sigma2, A2):
        return gauss(x, mu1, sigma1, A1)+gauss(x, mu2, sigma2, A2)

    """""
    Gaussian fitting parameters recognized in each file
    """""
    first_centroid = 0.004
    second_centroid = 0.01
    centroid = []
    centroid += (first_centroid, second_centroid)

    sigma = [0.001, 0.001]

    height = [1, 1]

    p = []

    p = [first_centroid, sigma[0], height[0],
         second_centroid, sigma[1], height[0]]
    try:
        popt, pcov = curve_fit(bimodal_gauss, centers, n2, p0=p[:])
        print(popt)
        new_y = []
        for x in centers:
            new_y.append(gauss(x, *popt[:3]))
        plt.plot(centers, new_y,
                 'w--', linewidth=1)
        new_y = []
        for x in centers:
            new_y.append(gauss(x, *popt[3:]))
        plt.plot(centers, new_y,
                 'b--', linewidth=1)
        new_y = []
        for x in centers:
            new_y.append(bimodal_gauss(x, *popt))
        label = r'$\mathrm{Histogram\ of\ speed\ two\ Gaussians:}$' + "\n" + r'$\mu1={: .4f}\pm{: .4f}$, $\sigma1={: .4f}\pm{: .4f}$'.format(
            popt[0], np.sqrt(pcov[0, 0]), abs(popt[1]), np.sqrt(pcov[1, 1])) + "\n" + r'$\mu2={: .4f}\pm{: .4f}$, $\sigma2={: .4f}\pm{: .4f}$'.format(popt[3], np.sqrt(pcov[3, 3]), abs(popt[4]), np.sqrt(pcov[4, 4]))
        plt.plot(centers, new_y,
                 'r--', linewidth=2, label=label)

        label = r'$\mathrm{Histogram\ of\ speed\ one\ Gaussian:}$' + "\n" + r'$\mu={: .4f}\pm{: .4f}$, $\sigma={: .4f}\pm{: .4f}$'.format(
                pars[0], np.sqrt(cov[0, 0]), pars[1], np.sqrt(cov[1, 1])) + "\n" + r'$\mathrm{number\ of\ robots:}\ \ %.d$' % (total_number_of_robots)
        plt.plot(centers, norm.pdf(centers, *pars),
                 'k--', linewidth=0.1, label=label)

    except RuntimeError:
        print("Could not find a double Gaussian fit")

    plt.xlabel("speed in m/s")
    plt.title("Robot histogram of speed. Arena diameter: " + arena_size + "m " +
              str(number_of_robots) + " kilobots per run, " + str(w_displacement_run_count) + " runs")
    plt.legend()
    plt.savefig(folder + "/Speed_" + str(number_of_robots) + "kilobots_" +
                str(w_displacement_run_count) + " runs.png", bbox_inches='tight', dpi=200, orientation="landscape")
    # plt.show(block=False)
    plt.close()


def n_sec_dist(directory, element, n_sec_distance_list, n, total_number_of_robots, number_of_robots, argos_ticks_per_second, sim_or_real):
    complete_filename = directory + "/" + element
    position_file = open(complete_filename, mode='rb')
    tsvin = csv.reader(position_file, delimiter='\t')
    window_size = 0
    tick_period = 0

    for row in tsvin:
        if(row[0] == "Robot id"):
            t1 = int(row[2].strip("T = ").strip("t = "))
            t0 = int(row[1].strip("T = ").strip("t = "))
            tick_period = t1 - t0
            break

    if(sim_or_real == "real"):
        window_size = 2 / tick_period
    else:
        window_size = argos_ticks_per_second / tick_period

    for row in tsvin:
        if(row[0] != "Robot id"):
            for i in range(1 + n * window_size, len(row) - 1):
                distance = 0.0
                for j in range(0, window_size*n, window_size):

                    [xi, yi] = row[i - j - window_size].split(",")
                    [xi, yi] = [float(xi), float(yi)]

                    [xf, yf] = row[i - j].split(",")
                    [xf, yf] = [float(xf), float(yf)]

                    distance += math.sqrt(((xf - xi)) **
                                          2 + ((yf - yi))**2) / float(n)
                if(distance < 0.025):
                    n_sec_distance_list.append(distance)
    total_number_of_robots += number_of_robots
    return(n_sec_distance_list, total_number_of_robots)


def displacement(folder, filename, current_sum_displacement, total_number_of_robots, num_robots, argos_ticks_per_second):
    complete_filename = folder + "/" + filename
    displacement_file = open(complete_filename, mode='rb')
    tsvin = csv.reader(displacement_file, delimiter='\t')

    average_displacement = []
    time_list = []
    expe_length = 0

    for row in tsvin:
        if(row[0] == "Robot id"):
            expe_length = len(row) - 2

            average_displacement = np.zeros(expe_length)
            time_list = np.zeros(expe_length)
            for i in range(1, len(row) - 1):
                timestep = row[i].strip("T = ")
                timestep = timestep.strip("t = ")
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
    time_list = [float(i)/argos_ticks_per_second for i in time_list]
    plt.plot(time_list, average_displacement,
             linewidth=0.5, linestyle='dashed')

    return (current_sum_displacement, total_number_of_robots, time_list)


def window_displacement(folder, position_filename, current_sum_w_displacement, total_number_of_robots, num_robots, window_size, argos_ticks_per_second, sim_or_real):
    complete_filename = folder + "/" + position_filename
    displacement_file = open(complete_filename, mode='rb')
    tsvin = csv.reader(displacement_file, delimiter='\t')

    average_w_displacement = []
    time_list = []
    expe_length = 0
    time_period = 0

    for row in tsvin:
        if(row[0] == "Robot id"):
            expe_length = len(row) - 1 - 2 * window_size

            average_w_displacement = np.zeros(expe_length)
            time_list = np.zeros(expe_length)
            time_period = int(row[2].strip("T = ").strip("t = ").strip('\t\n'))

            for i in range(1 + window_size, len(row) - window_size):
                timestep = row[i].strip("T = ")
                timestep = timestep.strip("t = ")
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
            for i in range(1 + window_size, len(row)-window_size):
                [xi, yi] = row[i-window_size].split(",")
                [xi, yi] = [float(xi), float(yi)]

                [xf, yf] = row[i].split(",")
                [xf, yf] = [float(xf), float(yf)]

                w_displacement = ((xf - xi)/window_size*2)**2 + \
                    ((yf - yi)/window_size*2)**2
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

    if(sim_or_real == "real"):
        tick_per_second = 2
    else:
        tick_per_second = argos_ticks_per_second

    time_list = [float(i)/tick_per_second for i in time_list]

    plt.plot(time_list, average_w_displacement,
             linewidth=0.5, linestyle='dashed')

    return (current_sum_w_displacement, total_number_of_robots, time_list, time_period)


def first_discovery(folder, time_filename, num_robots, total_number_of_robots, complete_time_dict, sim_or_real):
    complete_filename = folder + "/" + time_filename
    time_file = open(complete_filename, mode='rb')
    tsvin = csv.reader(time_file, delimiter='\t')

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
    if(sim_or_real == "real"):
        tick_per_second = 2
    else:
        tick_per_second = kilobot_ticks_per_second

    times = [float(i)/tick_per_second for i in times]
    plt.plot(times, values, linewidth=0.5, linestyle='dashed')
    total_number_of_robots += num_robots

    return (complete_time_dict, total_number_of_robots)


def first_information(folder, time_filename, num_robots, total_number_of_robots, complete_time_dict, sim_or_real):
    complete_filename = folder + "/" + time_filename
    time_file = open(complete_filename, mode='rb')
    tsvin = csv.reader(time_file, delimiter='\t')

    info_times = {}
    for row in tsvin:
        if(row[0] == "Robot id"):
            continue
        else:
            discovery = int(row[2])
            if(discovery > 0):
                if(not discovery in info_times):
                    info_times[discovery] = 1.0/num_robots
                else:
                    info_times[discovery] += 1.0/num_robots

                if(not discovery in complete_time_dict):
                    complete_time_dict[discovery] = 1.0
                else:
                    complete_time_dict[discovery] += 1.0

    times = info_times.keys()
    times.append(0)
    times = sorted(times)
    values = [0]
    cummulate = 0
    for key in times[1:]:
        cummulate += info_times[key]
        values.append(cummulate)

    if(sim_or_real == "real"):
        tick_per_second = 2
    else:
        tick_per_second = kilobot_ticks_per_second
    times = [float(i)/tick_per_second for i in times]

    plt.plot(times, values, linewidth=0.5, linestyle='dashed')
    total_number_of_robots += num_robots

    return (complete_time_dict, total_number_of_robots)


if __name__ == '__main__':
    main()
