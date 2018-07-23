import csv
import sys
import os

# with open('records.tsv', 'w') as tsvfile:
#     writer = csv.writer(tsvfile, delimiter='\t', newline='\n')
#     for record in SeqIO.parse("/home/fil/Desktop/420_2_03_074.fastq", "fastq"):
#         writer.writerow([record.id, record.seq, record.format("qual")])

number_of_args = len(sys.argv)
Kilobot_tick_per_second = 31


def print_help():
    print("usage : folder_path, sim or real, optionnal max time")


def main(folder, sim_or_real, maximum):
    num_robots = 0
    alpha = 0.0
    rho = 0.0
    # print(folder)
    multiplieur = 1.0
    if(sim_or_real == "real"):
        multiplieur = 31.0 / 2.0

    filename = folder.split("/")[-1]
    filename_pieces = filename.split("_")
    for element in filename_pieces:
        if(element.startswith("robots=")):
            num_robots = int(element.split("=")[-1])
        elif(element.startswith("alpha=")):
            alpha = float(element.split("=")[-1])
        elif(element.startswith("rho=")):
            rho = float(element.split("=")[1])
    # print(filename)
    # print(folder)

    result_folder = folder[:-len(filename)] + \
        "results_" + folder.split("/")[-2][12:]
    if(maximum < float("inf")):
        result_folder += "cropped_at_%d" % int(maximum / 31.0)
    # print(result_folder)

    if not os.path.exists(result_folder):
        os.mkdir(result_folder)
    new_filename = result_folder + "/result_bias0.0_levy%.2f_crw%.2f_pop%05d.dat" % (
        alpha, rho, num_robots)

    with open(new_filename, 'a') as tsvfile:
        writer = csv.writer(tsvfile, delimiter=' ')
        for subdir, _, files in os.walk(folder):
            for file_name in files:
                # print os.path.join(subdir, file)
                filepath = subdir + os.sep + file_name
                if filepath.endswith('time_results.tsv'):
                    line = time_synthesis(filepath, multiplieur, maximum)
                    writer.writerow(line)
                else:
                    continue
    return result_folder


def time_synthesis(filename, multiplieur, maximum):
    complete_filename = filename
    time_file = open(complete_filename, mode='rt')
    tsvin = csv.reader(time_file, delimiter='\t')

    first_ever_discovery = 10**100
    number_of_robots = 0.0
    number_of_information = 0.0
    number_of_discovery = 0.0
    convergence_time = 0.0
    line = []
    for row in tsvin:
        if(len(row) < 3):
            print("weird dude")
            continue
        else:
            if(row[0] == "Robot id"):
                continue
            else:
                row = [float(i) for i in row]
                number_of_robots += 1
                if(row[1] > 0):
                    value = int(round(row[1]*multiplieur))
                    if(value < maximum):
                        line.append(value)
                        number_of_discovery += 1
                        if(value < first_ever_discovery):
                            first_ever_discovery = value
                    else:
                        line.append("NaN")
                else:
                    line.append("NaN")
                if(row[2] > 0):
                    value = int(round(row[2]*multiplieur))
                    if(value < maximum):
                        number_of_information += 1
                        if(value > convergence_time):
                            convergence_time = value
    discovery_proportion = number_of_discovery / number_of_robots
    information_proportion = number_of_information / number_of_robots
    complete_information = 1

    if(number_of_information != number_of_robots):
        # print("everybody didnt get the info")
        complete_information = 0

    disconted_convergence_time = convergence_time - first_ever_discovery

    line = [complete_information, convergence_time,
            disconted_convergence_time, discovery_proportion, information_proportion] + line
    return line


if __name__ == '__main__':
    if (number_of_args < 2):
        print_help()
        exit(-1)

    folder = sys.argv[1]
    sim_or_real = sys.argv[2]
    maximum = float("inf")
    if(len(sys.argv) > 3):
        maximum = float(sys.argv[3]) * 31.0
    if "results" in folder:
        print("folder = result")
    else:
        main(folder, sim_or_real, maximum)
