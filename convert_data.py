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
    print("usage : folder_path (without / at the end)")


def main():
    if (number_of_args < 1):
        print_help()
        exit(-1)

    num_robots = 0
    alpha = 0.0
    rho = 0.0
    folder = sys.argv[1]
    filename = folder.split("/")[-1]
    filename = filename.split("_")
    for element in filename:
        if(element.startswith("robots=")):
            num_robots = int(element.split("=")[-1])
        elif(element.startswith("alpha=")):
            alpha = float(element.split("=")[-1])
        elif(element.startswith("rho=")):
            rho = float(element.split("=")[1])

    if not os.path.exists("experiments/results/"):
        os.mkdir("experiments/results/")
    new_filename = "experiments/results/result_bias0.0_levy%.2f_crw%.2f_pop0%04d.dat" % (
        alpha, rho, num_robots)

    with open(new_filename, 'a') as tsvfile:
        writer = csv.writer(tsvfile, delimiter=' ')
        for element in os.listdir(folder):
            if element.endswith('time_results.tsv'):
                line = time_synthesis(folder, element)
                writer.writerow(line)
            else:
                continue


def time_synthesis(folder, filename):
    complete_filename = folder + "/" + filename
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
                row = [int(i) for i in row]
                number_of_robots += 1
                if(row[1] != 0):
                    line.append(row[1])
                    number_of_discovery += 1
                    if(row[1] < first_ever_discovery):
                        first_ever_discovery = row[1]
                else:
                    line.append("NaN")
                if(row[2] != 0):
                    number_of_information += 1
                    if(row[2] > convergence_time):
                        convergence_time = row[2]
    discovery_proportion = number_of_discovery / number_of_robots
    information_proportion = number_of_information / number_of_robots
    complete_information = 1

    if(number_of_information != number_of_robots):
        print("everybody didnt get the info")
        complete_information = 0

    disconted_convergence_time = convergence_time - first_ever_discovery

    line = [complete_information, convergence_time,
            disconted_convergence_time, discovery_proportion, information_proportion] + line
    return line


main()
