import csv
import sys
import os

number_of_args = len(sys.argv)
Kilobot_tick_per_second = 31

def print_help():
    print("usage : folder_path, number of robot per run, argos ticks per second")


def main():
    if (number_of_args < 3):
        print_help()
        exit(-1)

    folder = sys.argv[1]
    number_of_robots = int(sys.argv[2])

    current_sum_displacement = []
    total_number_of_robots = 0
    displacement_run_count = 0



    for element in os.listdir(folder):
        if element.endswith('displacement.tsv'):

        else:
            continue
