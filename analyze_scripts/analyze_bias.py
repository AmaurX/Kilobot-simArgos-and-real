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
    print("usage : folder_path,  sim or real")


def main():
    """
    This script take a folder of processed experiments data, from a calibration run (where robots are asked to go straight) 
    It first applies a low_pass filter on the position of all robots, then it produces plots that analyze the bias in the turning of the robots, based on a differential drive model
    The results can be used to tune the ARGoS simulator.
    The time window used here is defined in the function find_bias
    """
    number_of_args = len(sys.argv)

    plt.figure(num=1, figsize=(12, 6), dpi=160, facecolor='w', edgecolor='k')
    plt.figure(num=2, figsize=(12, 6), dpi=160, facecolor='w', edgecolor='k')
    plt.figure(num=3, figsize=(12, 6), dpi=160, facecolor='w', edgecolor='k')
    plt.figure(num=4, figsize=(12, 6), dpi=160, facecolor='w', edgecolor='k')

    if (number_of_args < 2):
        print_help()
        exit(-1)

    folder = sys.argv[1]
    sim_or_real = sys.argv[2]

    if(sim_or_real != "sim" and sim_or_real != "real"):
        print("ERROR: you must specify if this is sim or real as second argument")
        exit(-1)
    left_bias_list = []
    right_bias_list = []
    speed_list = []
    omega_list = []
    info_list = []
    for directory, _, files in os.walk(folder):
        for element in files:
            if element.endswith('position.tsv'):
                (left_bias_list, right_bias_list, speed_list, omega_list, info_list) = find_bias(directory, element,
                                                                                                 left_bias_list, right_bias_list, speed_list, omega_list, info_list)

            else:
                continue
    both_sides = left_bias_list+right_bias_list
    for mylist in [left_bias_list, right_bias_list, speed_list, both_sides]:
        if(mylist == speed_list):
            mylist = [item for sublist in mylist for item in sublist]
        n2, bins, _ = plt.hist(
            mylist, bins='auto', density=1)
        centers = (0.5*(bins[1:]+bins[:-1]))
        pars, cov = curve_fit(lambda total_list, mu, sig: norm.pdf(
            total_list, loc=mu, scale=sig), centers, n2, p0=[0, 1])
        axes = plt.gca()
        axes.set_xlim([-0.005, 0.025])

        label = r'$\mathrm{Histogram\ of\ speed\ bias:}$' + "\n" + r'$\mu={: .4e}\pm{: .4e}$, $\sigma={: .4e}\pm{: .4e}$'.format(
                pars[0], np.sqrt(cov[0, 0]), pars[1], np.sqrt(cov[1, 1]))
        plt.plot(centers, norm.pdf(centers, *pars),
                 'r--', linewidth=1, label=label)

        side = ""
        if(mylist == left_bias_list):
            side = "left"
        elif(mylist == right_bias_list):
            side = "right"
        elif(mylist == both_sides):
            side = "both_sides"
        if(mylist != speed_list):
            plt.title("Robot histogram of speed bias (%s). " % (side) +
                      str(len(mylist)) + " measures")
        else:
            plt.title("Robot histogram of linear speed. " +
                      str(len(mylist)) + " measures")
        plt.xlabel("speed in m/s")
        plt.legend()

        plt.savefig(folder + "/Speed_bias_" + side + "_" + str(len(mylist)) +
                    "_measures.png", bbox_inches='tight', dpi=200, orientation="landscape")
        # plt.show(block=False)
        plt.close()


def sub(x, offset):
    return x - offset


def find_bias(directory, element, left_bias_list, right_bias_list, speed_list, omega_list, info_list):
    """
    Applies here the low_pass filter function
    Dt is the time window
     
    """
    
    complete_filename = directory + "/" + element
    position_file = open(complete_filename, mode='rb')
    tsvin = csv.reader(position_file, delimiter='\t')
    Dt = 2.0
    tick_per_second = 2

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

                if(V >= 0.04 or Omega >= 1.2):
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
