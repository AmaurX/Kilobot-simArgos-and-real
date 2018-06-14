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
    print("usage : folder_path,  sim or real  argos ticks per second")


def main():
    number_of_args = len(sys.argv)

    plt.figure(num=1, figsize=(12, 6), dpi=160, facecolor='w', edgecolor='k')

    if (number_of_args < 3):
        print_help()
        exit(-1)

    folder = sys.argv[1]
    arena_size = "0.95"
    sim_or_real = sys.argv[2]
    argos_ticks_per_second = int(sys.argv[3])
    total_number_of_robots = 0

    if(sim_or_real != "sim" and sim_or_real != "real"):
        print("ERROR: you must specify if this is sim or real as third argument")
        exit(-1)

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
                                                                           n_sec_distance_list, n, total_number_of_robots, argos_ticks_per_second, sim_or_real)

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
              str(total_number_of_robots) + " kilobots on " + str(w_displacement_run_count) + " runs")
    plt.legend()
    plt.savefig(folder + "/Speed_" + str(total_number_of_robots) + "_kilobots_" +
                str(w_displacement_run_count) + "_runs.png", bbox_inches='tight', dpi=200, orientation="landscape")
    # plt.show(block=False)
    plt.close()


def n_sec_dist(directory, element, n_sec_distance_list, n, total_number_of_robots, argos_ticks_per_second, sim_or_real):
    complete_filename = directory + "/" + element
    position_file = open(complete_filename, mode='rb')
    tsvin = csv.reader(position_file, delimiter='\t')
    window_size = 0
    tick_period = 0
    number_of_robots = 0
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
            number_of_robots += 1
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


if __name__ == '__main__':
    main()
