import csv
import matplotlib.pyplot as plt
import argparse
import os
from scipy.stats import norm
import math
from scipy.optimize import curve_fit
import numpy as np

image_folder = "images_initial_distance/"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-f", "--folder",
                    help="path to the experiment folder")

    args = vars(ap.parse_args())

    total_list = []
    target_distance = []
    number_of_experiment = 0
    folder = args["folder"]
    for directory, dirs, files in os.walk(folder):
        for filename in files:
            filepath = directory + os.sep + filename
            if(filename.endswith("initial_distances.tsv")):
                initial_distance_file = open(filepath, 'r')
                initial_distance = csv.reader(
                    initial_distance_file, delimiter="\t")
                for row in initial_distance:
                    total_list.extend(row[1:])
                    target_distance.append(row[0])
                    number_of_experiment += 1

    plt.figure(figsize=(10, 10))
    total_list = map(float, total_list)
    # total_list = filter(is_smaller_than_025, total_list)
    n = len(total_list)
    # print(bins)
    # bins = 3 * int(round(pow(n, 1.0/3.0)))
    n2, bins, _ = plt.hist(total_list, bins='auto',  density=1)

    # (mu, sigma) = norm.fit(total_list)
    # y = norm.pdf(bins, mu, sigma)
    # l = plt.plot(bins, y, 'r--', linewidth=2)

    centers = (0.5*(bins[1:]+bins[:-1]))
    pars, cov = curve_fit(lambda total_list, mu, sig: norm.pdf(
        total_list, loc=mu, scale=sig), centers, n2, p0=[0, 1])

    axes = plt.gca()
    # axes.set_xlim([0.0, 0.22])
    axes.set_xlim([0, 1.0])

    plt.plot(centers, norm.pdf(centers, *pars),
             'k--', linewidth=2, label='optimized fit')

    plt.title(r'$\mathrm{Histogram\ of\ initial\ distances:}$' + "\n" + r'$\mu={: .4f}\pm{: .4f}$, $\sigma={: .4f}\pm{: .4f}$'.format(
        pars[0], np.sqrt(cov[0, 0]), pars[1], np.sqrt(cov[1, 1])) + "\n" + r'$\mathrm{number\ of\ values:}\ \ %.d$' % (n))
    plt.legend()
    plt.xlabel('distance (in meters)')
    # plt.title((
    #     r'$\mathrm{Histogram\ of\ communication\ distance:}\ \mu=%.3f,\ \sigma=%.3f$' % (mu, sigma)) + "\n" + (
    #     r'$\mathrm{number\ of\ values:}\ \ %.d$' % (n)))
    # plt.show()
    folder = folder.strip("/")
    result_folder = image_folder + folder[:-len(folder.split("/")[-1])]
    if not os.path.exists(result_folder):
        os.mkdir(result_folder)

    plt.savefig(image_folder + folder.strip("/") + "_distance.png")

    plt.figure(figsize=(10, 10))
    target_distance = map(float, target_distance)
    # total_list = filter(is_smaller_than_025, total_list)
    n = len(target_distance)
    # print(bins)
    # bins = 3 * int(round(pow(n, 1.0/3.0)))
    n2, bins, _ = plt.hist(target_distance, bins='auto',  density=1)

    # (mu, sigma) = norm.fit(target_distance)
    # y = norm.pdf(bins, mu, sigma)
    # l = plt.plot(bins, y, 'r--', linewidth=2)

    centers = (0.5*(bins[1:]+bins[:-1]))
    pars, cov = curve_fit(lambda target_distance, mu, sig: norm.pdf(
        target_distance, loc=mu, scale=sig), centers, n2, p0=[0, 1])

    axes = plt.gca()
    # axes.set_xlim([0.0, 0.22])
    axes.set_xlim([0, 1.0])

    plt.plot(centers, norm.pdf(centers, *pars),
             'k--', linewidth=2, label='optimized fit')

    plt.title(r'$\mathrm{Histogram\ of\ initial\ distances\ from\ target:}$' + "\n" + r'$\mu={: .4f}\pm{: .4f}$, $\sigma={: .4f}\pm{: .4f}$'.format(
        pars[0], np.sqrt(cov[0, 0]), pars[1], np.sqrt(cov[1, 1])) + "\n" + r'$\mathrm{number\ of\ values:}\ \ %.d$' % (n))
    plt.legend()
    plt.xlabel('distance (in meters)')
    # plt.title((
    #     r'$\mathrm{Histogram\ of\ communication\ distance:}\ \mu=%.3f,\ \sigma=%.3f$' % (mu, sigma)) + "\n" + (
    #     r'$\mathrm{number\ of\ values:}\ \ %.d$' % (n)))
    # plt.show()
    folder = folder.strip("/")
    result_folder = image_folder + folder[:-len(folder.split("/")[-1])]
    if not os.path.exists(result_folder):
        os.mkdir(result_folder)

    plt.savefig(image_folder + folder.strip("/") + "_target_distance.png")


if __name__ == '__main__':
    main()
