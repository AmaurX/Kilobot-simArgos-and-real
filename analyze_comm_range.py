import csv
import matplotlib.pyplot as plt
import argparse
import os
from scipy.stats import norm
import math
from scipy.optimize import curve_fit
import numpy as np


def is_smaller_than_025(f):
    if(f < 0.22):
        return True
    return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-f", "--folder",
                    help="path to the experiment folder")

    args = vars(ap.parse_args())

    total_list = []
    number_of_experiment = 0
    folder = args["folder"]
    for directory, dirs, files in os.walk(folder):
        for filename in files:
            filepath = directory + os.sep + filename
            if(filename.endswith("comm_range.tsv")):
                comm_range_file = open(filepath, 'r')
                comm_range = csv.reader(
                    comm_range_file, delimiter="\t")
                for row in comm_range:
                    total_list.extend(row)
                    number_of_experiment += 1

    total_list = map(float, total_list)
    total_list = filter(is_smaller_than_025, total_list)
    print(number_of_experiment)
    n = len(total_list)
    print(n)
    # print(bins)
    # bins = 3 * int(round(pow(n, 1.0/3.0)))
    n2, bins, _ = plt.hist(total_list, bins='auto',  density=1)
    print(len(bins))

    # (mu, sigma) = norm.fit(total_list)
    # y = norm.pdf(bins, mu, sigma)
    # l = plt.plot(bins, y, 'r--', linewidth=2)

    centers = (0.5*(bins[1:]+bins[:-1]))
    pars, cov = curve_fit(lambda total_list, mu, sig: norm.pdf(
        total_list, loc=mu, scale=sig), centers, n2, p0=[0, 1])

    plt.plot(centers, norm.pdf(centers, *pars),
             'k--', linewidth=2, label='optimized fit')

    plt.title(r'$\mathrm{Histogram\ of\ communication\ distance:}$' + "\n" + r'$\mu={: .4f}\pm{: .4f}$, $\sigma={: .4f}\pm{: .4f}$'.format(
        pars[0], np.sqrt(cov[0, 0]), pars[1], np.sqrt(cov[1, 1])) + "\n" + r'$\mathrm{number\ of\ values:}\ \ %.d$' % (n))
    plt.legend()
    plt.xlabel('distance (in meters)')
    # plt.title((
    #     r'$\mathrm{Histogram\ of\ communication\ distance:}\ \mu=%.3f,\ \sigma=%.3f$' % (mu, sigma)) + "\n" + (
    #     r'$\mathrm{number\ of\ values:}\ \ %.d$' % (n)))
    plt.show()


if __name__ == '__main__':
    main()
