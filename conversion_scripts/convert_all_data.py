import csv
import sys
import os
import conversion_scripts.convert_data as convert_data
# with open('records.tsv', 'w') as tsvfile:
#     writer = csv.writer(tsvfile, delimiter='\t', newline='\n')
#     for record in SeqIO.parse("/home/fil/Desktop/420_2_03_074.fastq", "fastq"):
#         writer.writerow([record.id, record.seq, record.format("qual")])

number_of_args = len(sys.argv)


def print_help():
    print("usage : overall experiment folder path, 'sim' or 'real', optionnal max time")


def main():
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
        return 0

    result_folder = ""
    for subdir, _, _ in os.walk(folder):
        if(subdir != folder and not "result" in subdir):
            result_folder = convert_data.main(subdir, sim_or_real, maximum)

    print("Done! Converted data are in %s" % result_folder)


if __name__ == '__main__':
    main()
