import matplotlib.pyplot as plt
import numpy as np
import csv
import sys
import os
from scipy import stats
import math
from scipy.optimize import curve_fit
from scipy.stats import norm
from scipy.signal import butter, lfilter, filtfilt
from scipy.signal import freqs, freqz

# default value
kilobot_ticks_per_second = 31
L = 0.025


def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a


def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = filtfilt(b, a, data)
    return y


def print_help():
    print("usage : folder_path,  sim or real  argos ticks per second")


def main():
    number_of_args = len(sys.argv)

    plt.figure(num=1, figsize=(12, 6), dpi=160, facecolor='w', edgecolor='k')
    plt.figure(num=2, figsize=(12, 6), dpi=160, facecolor='w', edgecolor='k')
    plt.figure(num=3, figsize=(12, 6), dpi=160, facecolor='w', edgecolor='k')

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
    left_bias_list = []
    right_bias_list = []
    speed_list = []
    omega_list = []
    info_list = []
    for directory, dirs, files in os.walk(folder):
        for element in files:
            if element.endswith('position.tsv'):
                (left_bias_list, right_bias_list, speed_list, omega_list, info_list) = find_bias(directory, element,
                                                                                                 left_bias_list, right_bias_list, speed_list, omega_list, info_list)

            else:
                continue
    for mylist in [left_bias_list, right_bias_list, speed_list]:
        if(mylist == speed_list):
            mylist = [item for sublist in mylist for item in sublist]
        n2, bins, _ = plt.hist(
            mylist, bins='auto', density=1)
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
            # popt, pcov = curve_fit(bimodal_gauss, centers, n2, p0=p[:])
            # print(popt)
            # new_y = []
            # for x in centers:
            #     new_y.append(bimodal_gauss(x, *popt))
            # label = r'$\mathrm{Histogram\ of\ speed\ two\ Gaussians:}$'
            # plt.plot(centers, new_y,
            #          'r--', linewidth=2, label=label)
            # new_y = []
            # label = r'$\mu1={: .4f}\pm{: .4f}$, $\sigma1={: .4f}\pm{: .4f}$'.format(
            #     popt[0], np.sqrt(pcov[0, 0]), abs(popt[1]), np.sqrt(pcov[1, 1]))
            # for x in centers:
            #     new_y.append(gauss(x, *popt[:3]))
            # plt.plot(centers, new_y,
            #          'g--', linewidth=1, label=label)
            # new_y = []
            # label = r'$\mu2={: .4f}\pm{: .4f}$, $\sigma2={: .4f}\pm{: .4f}$'.format(
            #     popt[3], np.sqrt(pcov[3, 3]), abs(popt[4]), np.sqrt(pcov[4, 4]))
            # for x in centers:
            #     new_y.append(gauss(x, *popt[3:]))
            # plt.plot(centers, new_y,
            #          'b--', linewidth=1, label=label)

            label = r'$\mathrm{Histogram\ of\ speed\ bias:}$' + "\n" + r'$\mu={: .4e}\pm{: .4e}$, $\sigma={: .4e}\pm{: .4e}$'.format(
                pars[0], np.sqrt(cov[0, 0]), pars[1], np.sqrt(cov[1, 1])) + "\n" + r'$\mathrm{number\ of\ robots:}\ \ %.d$' % (total_number_of_robots)
            plt.plot(centers, norm.pdf(centers, *pars),
                     'r--', linewidth=1, label=label)

        except RuntimeError:
            print("Could not find a double Gaussian fit")
        side = ""
        if(mylist == left_bias_list):
            side = "_left"
        elif(mylist == right_bias_list):
            side = "_right"
        plt.xlabel("speed in m/s")
        plt.title("Robot histogram of speed bias (%s). Arena diameter: " % (side) + arena_size + "m " +
                  str(len(mylist)) + " measures")
        plt.legend()
        plt.savefig(folder + "/Speed_bias_" + side + "_" + str(len(mylist)) +
                    "_measures.png", bbox_inches='tight', dpi=200, orientation="landscape")
        # plt.show(block=False)
        plt.close()


def sub(x, offset):
    return x - offset


def find_bias(directory, element, left_bias_list, right_bias_list, speed_list, omega_list, info_list):
    complete_filename = directory + "/" + element
    position_file = open(complete_filename, mode='rb')
    tsvin = csv.reader(position_file, delimiter='\t')
    tick_period = 0
    Dt = 2.0
    tick_per_second = 2
    # for row in tsvin:
    #     if(row[0] == "Robot id"):
    #         t1 = int(row[2].strip("T = ").strip("t = "))
    #         t0 = int(row[1].strip("T = ").strip("t = "))
    #         tick_period = t1 - t0
    #         break
    count = 0
    for row in tsvin:
        if(row[0] != "Robot id"):
            speed_list.append([])
            omega_list.append([])
            info_list.append([])
            cutoff = .3  # cutoff frequency in Hz
            fs = 2  # sampling frequency in Hz
            order = 2  # order of filter

            # print sticker_data.ps1_dxdt2

            b, a = butter_lowpass(cutoff, fs, order)

            # Plot the frequency response.
            # w, h = freqz(b, a, worN=8000)
            # plt.subplot(2, 1, 1)
            # plt.plot(0.5*fs*w/np.pi, np.abs(h), 'b')
            # plt.plot(cutoff, 0.5*np.sqrt(2), 'ko')
            # plt.axvline(cutoff, color='k')
            # plt.xlim(0, 0.5*fs)
            # plt.title("Lowpass Filter Frequency Response")
            # plt.xlabel('Frequency [Hz]')
            # plt.grid()
            # plt.show()
            row = row[1:]

            for i in range(len(row)):
                [xi, yi] = row[i].split(",")
                [xi, yi] = [float(xi), float(yi)]
                row[i] = [xi, yi]
            row = np.array(row)
            # plt.plot(row[:, 0], 'r--', linewidth=2)
            # plt.plot(row[:, 1], 'r--', linewidth=2)

            for i in [0, 1]:
                offset = row[0, i]
                row[:, i] = row[:, i] - offset
                row[:, i] = butter_lowpass_filter(row[:, i], cutoff, fs, order)
                row[:, i] = row[:, i] + offset

            # plt.plot(row[:, 0], 'b--')
            # plt.plot(row[:, 1], 'b--')

            # plt.show()
            # for i in range(1, int(len(row)-(Dt * tick_per_second)), int(Dt * tick_per_second)):
            #     V = 0.0
            #     Omega = 0.0

            #     [xi, yi] = row[i - 1]

            #     [xf, yf] = row[i]
            #     angle = math.atan2((yf-yi), (xf-xi))

            #     [xt, yt] = row[i + int(Dt * tick_per_second)]

            #     angle2 = math.atan2((yt-yf), (xt-xf))

            #     B = math.sqrt(math.pow(xt-xf, 2) + math.pow(yt-yf, 2))
            #     theta_diff = angle - angle2
            #     if(theta_diff > math.pi):
            #         theta_diff -= math.pi
            #     elif(theta_diff <= -math.pi):
            #         theta_diff += math.pi
            #     R = 0
            #     if(theta_diff != 0):
            #         Omega = 2 * theta_diff / Dt
            #         V = (theta_diff * B) / (Dt * math.sin(theta_diff))
            #         R = abs(B / (2.0 * math.sin(theta_diff)))

            #     else:
            #         Omega = 0.0
            #         V = B / Dt
            #     if(V >= 0.04):
            #         print("WARNING: V = %.3f, Omega = %.4f" %
            #               (V, Omega))
            #     else:
            #         Vl = - (Omega * L) / 2.0
            #         Vr = + (Omega * L) / 2.0
            #         left_bias_list.append(Vl)
            #         right_bias_list.append(Vr)
            #         speed_list[count].append(V)
            #         omega_list[count].append(Omega)
            #         info_list[count].append([R, angle])

            for i in range(1, int(len(row)-(Dt * tick_per_second)), int(Dt * tick_per_second)):
                V = 0.0
                Omega = 0.0

                [xi, yi] = row[i - 1]

                [xf, yf] = row[i]
                angle = math.atan2((yf-yi), (xf-xi))

                [xt, yt] = row[i + int(Dt * tick_per_second)]
                [xtf, ytf] = row[i + int(Dt * tick_per_second) - 1]
                angle2 = math.atan2((yt-ytf), (xt-xtf))

                B = math.sqrt(math.pow(xt-xf, 2) + math.pow(yt-yf, 2))
                theta_diff = angle - angle2
                if(theta_diff > math.pi):
                    theta_diff -= math.pi
                elif(theta_diff <= -math.pi):
                    theta_diff += math.pi
                R = 0

                V = B/Dt
                Omega = theta_diff/Dt

                if(V >= 0.04):
                    print("WARNING: V = %.3f, Omega = %.4f" %
                          (V, Omega))
                else:
                    Vl = V - (Omega * L) / 2.0
                    Vr = V + (Omega * L) / 2.0
                    left_bias_list.append(Vl)
                    right_bias_list.append(Vr)
                    speed_list[count].append(V)
                    omega_list[count].append(Omega)
                    info_list[count].append([R, angle])

            count += 1
        # plt.show()
        # plt.close()
    return left_bias_list, right_bias_list, speed_list, omega_list, info_list


if __name__ == '__main__':
    main()