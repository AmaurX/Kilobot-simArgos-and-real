import matplotlib.pyplot as plt
import numpy as np
import csv
import sys
import os
from scipy import stats
import math
from scipy.optimize import curve_fit
from scipy.stats import norm
import seaborn as sns
import pandas as pd

# default value
kilobot_ticks_per_second = 31
my_dict = dict()
# my_dict = dict({'10': {'0.9': {'1.4': 6.351612311609518e-05, '1.6': 6.169517731712202e-05, '1.0': 6.769525293224953e-05, '1.2': 6.696551568123494e-05, '1.8': 6.191230235583315e-05, '2.0': 6.252161741701128e-05}, '0.0': {'1.4': 4.493446009396877e-05, '1.6': 4.143595815148038e-05, '1.0': 5.639997748844838e-05, '1.2': 5.132829207224097e-05, '1.8': 3.9328158006585945e-05, '2.0': 3.687855602634013e-05}, '0.3': {'1.4': 5.081332735830571e-05, '1.6': 4.794598440005397e-05, '1.0': 5.9781819776411144e-05, '1.2': 5.4051802122823445e-05, '1.8': 4.5085776180601636e-05, '2.0': 4.361287109459804e-05}, '0.6': {'1.4': 5.624302899860774e-05, '1.6': 5.3993804668035006e-05, '1.0': 6.445482195184809e-05, '1.2': 5.885361534186477e-05, '1.8': 5.267783892173749e-05, '2.0': 5.146234392116877e-05}, '0.15': {'1.4': 4.7639578367129724e-05, '1.6': 4.4883836770846024e-05, '1.0': 5.810128524664247e-05, '1.2': 5.3628565919141046e-05, '1.8': 4.247400493909832e-05, '2.0': 3.956771720265378e-05}, '0.99': {'1.4': 6.892423077290912e-05, '1.6': 6.961834806597853e-05, '1.0': 7.187000856234634e-05, '1.2': 7.210970879707219e-05, '1.8': 6.782541304116122e-05, '2.0': 6.770661843326982e-05}, '0.75': {'1.4': 5.827356535695851e-05, '1.6': 5.7938517879226516e-05, '1.0': 6.520234910922866e-05, '1.2': 6.284686994503807e-05, '1.8': 5.6790743324605213e-05, '2.0': 5.5239115517553786e-05}, '0.95': {'1.4': 6.529255906085738e-05, '1.6': 6.62793567408697e-05, '1.0': 6.783204839608881e-05, '1.2': 6.807659340756074e-05, '1.8': 6.470346231583974e-05, '2.0': 6.464880212364814e-05}, '0.45': {'1.4': 5.394367730779668e-05, '1.6': 5.04844957173157e-05, '1.0': 6.130348880019838e-05, '1.2': 5.51953134637527e-05, '1.8': 4.863399510404761e-05, '2.0': 4.6443034178774485e-05}}, '30': {'0.9': {'1.4': 5.6782936981405305e-05, '1.6': 5.590162702794155e-05, '1.0': 5.9802153931116186e-05, '1.2': 5.809846242438078e-05, '1.8': 5.510866330518858e-05, '2.0': 5.502359419835788e-05}, '0.0': {'1.4': 4.3225167755268105e-05, '1.6': 4.000452115067074e-05, '1.0': 5.264098279760855e-05, '1.2': 4.721003675776156e-05, '1.8': 3.76123897395217e-05, '2.0': 3.5876583029826166e-05}, '0.3': {'1.4': 4.753288151422005e-05, '1.6': 4.418531242536673e-05, '1.0': 5.486562032637343e-05, '1.2': 5.024841501635256e-05, '1.8': 4.2034815636459114e-05, '2.0': 4.1201863692010564e-05}, '0.6': {'1.4': 5.174630297559918e-05, '1.6': 4.935693888087808e-05, '1.0': 5.726674799755391e-05, '1.2': 5.3578809842605744e-05, '1.8': 4.776973770448306e-05, '2.0': 4.670277332271682e-05}, '0.15': {'1.4': 4.474263616887717e-05, '1.6': 4.2201801135919897e-05, '1.0': 5.314669145420212e-05,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    #  '1.2': 4.89998630207656e-05, '1.8': 3.9590656888010904e-05, '2.0': 3.800698845156243e-05}, '0.99': {'1.4': 6.190393086588912e-05, '1.6': 6.0853443020773104e-05, '1.0': 6.269646164172277e-05, '1.2': 6.203141744634666e-05, '1.8': 6.018657073436824e-05, '2.0': 6.066911868510381e-05}, '0.75': {'1.4': 5.4002107574110775e-05, '1.6': 5.259946319805288e-05, '1.0': 5.810568527808528e-05, '1.2': 5.639448593139326e-05, '1.8': 5.115530282953612e-05, '2.0': 5.103248873918474e-05}, '0.95': {'1.4': 5.870773922514771e-05, '1.6': 5.8150522078967755e-05, '1.0': 6.118814977360073e-05, '1.2': 6.080339701978001e-05, '1.8': 5.756686042014212e-05, '2.0': 5.6511859095927306e-05}, '0.45': {'1.4': 4.9287563639105675e-05, '1.6': 4.704465982472984e-05, '1.0': 5.6087364371531394e-05, '1.2': 5.148568838202293e-05, '1.8': 4.49408534241792e-05, '2.0': 4.376180012067852e-05}}, '20': {'0.9': {'1.4': 6.068393978983838e-05, '1.6': 5.8427839256117965e-05, '1.0': 6.310892245219181e-05, '1.2': 6.121529076038824e-05, '1.8': 5.773410867928697e-05, '2.0': 5.84799741438568e-05}, '0.0': {'1.4': 4.414997116264077e-05, '1.6': 4.08660696920935e-05, '1.0': 5.417080040060961e-05, '1.2': 4.821356611130134e-05, '1.8': 3.8856753283867394e-05, '2.0': 3.592504643960435e-05}, '0.3': {'1.4': 4.891458886059741e-05, '1.6': 4.5443220190186896e-05, '1.0': 5.638304502971338e-05, '1.2': 5.286534305066853e-05, '1.8': 4.364813787158546e-05, '2.0': 4.172348947545774e-05}, '0.6': {'1.4': 5.338904188280404e-05, '1.6': 5.131236420138038e-05, '1.0': 5.9356250450439676e-05, '1.2': 5.5939301995864365e-05, '1.8': 4.987841780750731e-05, '2.0': 4.8195181993879096e-05}, '0.15': {'1.4': 4.66688748649653e-05, '1.6': 4.307124230087467e-05, '1.0': 5.434179237693389e-05, '1.2': 5.095422634316578e-05, '1.8': 4.0780048655703936e-05, '2.0': 3.950596576897428e-05}, '0.99': {'1.4': 6.375631742144338e-05, '1.6': 6.42631834809476e-05, '1.0': 6.623782425527266e-05, '1.2': 6.511005209654742e-05, '1.8': 6.44868410161315e-05, '2.0': 6.343075321307617e-05}, '0.75': {'1.4': 5.6634798690017525e-05, '1.6': 5.4493849018071845e-05, '1.0': 6.124205435380732e-05, '1.2': 5.8479214693489915e-05, '1.8': 5.38941255308108e-05, '2.0': 5.248449794757115e-05}, '0.95': {'1.4': 6.198039890043665e-05, '1.6': 6.128602416640711e-05, '1.0': 6.423646497376918e-05, '1.2': 6.293559837278225e-05, '1.8': 6.072660279317512e-05, '2.0': 6.0142828502523085e-05}, '0.45': {'1.4': 5.0728716589845804e-05, '1.6': 4.830025432621489e-05, '1.0': 5.826727121312816e-05, '1.2': 5.4829384015102343e-05, '1.8': 4.6742433594930794e-05, '2.0': 4.491143755822193e-05}}})


def print_help():
    print("usage : folder_path, sim or real ,window size (for windowed_MSD)")


def main():
    number_of_args=len(sys.argv)

    if (number_of_args < 4):
        print_help()
        exit(-1)

    folder=sys.argv[1]
    sim_or_real=sys.argv[2]
    window_size=int(sys.argv[3]) * 2

    if(sim_or_real != "sim" and sim_or_real != "real"):
        print("ERROR: you must specify if this is sim or real as third argument")
        exit(-1)

    if(my_dict):
        total_dict=my_dict
    else:
        total_dict=dict()
        number_dict=dict()
        count=1
        robots_already_done=[]
        for directory, dirs, files in os.walk(folder):
            if(directory == folder):
                for a_file in files:
                    if a_file.endswith(".pickle"):
                        pickle_file=os.path.join(directory, a_file)
                        data_frame=pd.read_pickle(pickle_file)
                        elements=a_file.split("_")
                        number_of_robots_here=elements[1]
                        new_dict=data_frame.to_dict()
                        total_dict[number_of_robots_here]=new_dict
                        robots_already_done.append(number_of_robots_here)

        for directory, dirs, files in os.walk(folder):
            n="0"
            rho=-1.0
            alpha=-1.0
            elements=directory.split("_")
            passing=False
            for e in elements:
                if e.startswith("robots"):
                    n=e.split("=")[-1]
                    if(n in robots_already_done):
                        passing=True
                    if(not total_dict.has_key(n)):
                        total_dict[n]=dict()
                        number_dict[n]=dict()

                if(e.startswith("rho")):
                    rho=float(e.split("=")[-1])
                if(e.startswith("alpha")):
                    alpha=float(e.split("=")[-1])
            if(passing):
                continue
            print(str(count) + " : " + directory)

            if(n == "0" or rho == -1.0 or alpha == -1.0):
                continue
            rho_str=str(rho)
            alpha_str=str(alpha)
            if(not total_dict[n].has_key(rho_str)):
                total_dict[n][rho_str]=dict()
                number_dict[n][rho_str]=dict()
            mean_wmsd=0.0
            number_of_experiments=0
            for one_file in files:
                if one_file.endswith('position.tsv'):
                    (mean_wmsd, number_of_experiments)=window_displacement(
                        os.path.join(directory, one_file), mean_wmsd, number_of_experiments, window_size, int(n))

            if(number_dict[n][rho_str].has_key(alpha_str)):
                previous_number=number_dict[n][rho_str][alpha_str]
                total_dict[n][rho_str][alpha_str] *= previous_number
                total_dict[n][rho_str][alpha_str] += mean_wmsd * \
                    number_of_experiments
                total_dict[n][rho_str][alpha_str] /= previous_number + \
                    number_of_experiments
                number_dict[n][rho_str][alpha_str] += number_of_experiments
            else:
                total_dict[n][rho_str][alpha_str]=mean_wmsd
                number_dict[n][rho_str][alpha_str]=number_of_experiments
            count += 1

    # print(total_dict)
    for key, value in total_dict.iteritems():
        fig=plt.figure(figsize = (12, 8))
        dataFrame=pd.DataFrame.from_dict(value)
        reversed_df=dataFrame.iloc[::-1]
        ax=sns.heatmap(reversed_df, annot = True, fmt = ".2e", vmin=0.0000335, vmax=0.0000751)
        ax.set_title("Heatmap of WMSD for %s robots" % (key))
        ax.set_ylabel("alpha")
        ax.set_xlabel("rho")
        file_name="%s/WMSD_%s_robots_heatmap.png" % (folder, key)
        plt.savefig(file_name)
        reversed_df.to_pickle(file_name[:-4] + ".pickle")
    # for i in range(len(current_sum_w_displacement)):
    #     current_sum_w_displacement[i] = current_sum_w_displacement[i] / \
    #         float(w_total_number_of_robots)
    # time_list = time_list[:len(current_sum_w_displacement)]

    # slope, intercept, r_value, p_value, std_err = stats.linregress(
    #     time_list, current_sum_w_displacement)

    # linear_approx = [slope * i + intercept for i in time_list]
    # plt.plot(time_list, linear_approx, color='r', linewidth=2, linestyle=":",
    #          label="slope : " + "%.4e" % slope + " r^2 = " + "%.4f" % (r_value**2))
    # plt.plot(time_list, current_sum_w_displacement, color='b', linewidth=3,
    #          label="Window MSD (window = " + str(window_size/2) + " seconds) overtime on " + str(w_total_number_of_robots) + " robots")

    # plt.xlabel("Time in seconds")
    # plt.ylabel("MSD in m^2")
    # plt.title("Arena diameter: " + arena_size + "m " +
    #           str(number_of_robots) + " kilobots per run, " + str(w_displacement_run_count) + " runs")
    # plt.legend()
    # plt.savefig(folder + "/Window_MSD_" + str(number_of_robots) + "kilobots_" +
    #             str(w_displacement_run_count) + " runs.png", bbox_inches='tight', dpi=200, orientation="landscape")
    # # plt.show(block=False)
    # plt.close()


def window_displacement(position_filename, mean_wmsd, number_of_experiments, window_size, num_robots):
    displacement_file=open(position_filename, mode = 'rb')
    tsvin=csv.reader(displacement_file, delimiter = '\t')

    average_w_displacement=[]
    time_list=[]
    expe_length=0
    time_period=0

    for row in tsvin:
        if(row[0] == "Robot id"):
            expe_length=len(row) - 1 - 2 * window_size

            average_w_displacement=np.zeros(expe_length)
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
                [xi, yi]=row[i-window_size].split(",")
                [xi, yi]=[float(xi), float(yi)]

                [xf, yf]=row[i].split(",")
                [xf, yf]=[float(xf), float(yf)]

                w_displacement=((xf - xi)/window_size*2)**2 + \
                    ((yf - yi)/window_size*2)**2
                w_displacement /= num_robots

                average_w_displacement[i-1 - window_size] += w_displacement
    number_of_value=len(average_w_displacement)
    mean=0.0
    for i in average_w_displacement:
        mean=mean + i/number_of_value

    if(number_of_experiments == 0):
        mean_wmsd=mean
        number_of_experiments += 1
    else:
        mean_wmsd *= number_of_experiments
        mean_wmsd += mean
        number_of_experiments += 1
        mean_wmsd /= float(number_of_experiments)

    return (mean_wmsd, number_of_experiments)


if __name__ == '__main__':
    main()
