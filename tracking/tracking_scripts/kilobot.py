import math
import csv
from scipy import spatial
from smartquadtree import Quadtree
import matplotlib.pyplot as plt
import cv2
import itertools
from time import gmtime, strftime
import os


class Kilobot(object):

    kilobot_list = []
    temp_kilobot_list = []
    potential_target_list = []
    number_of_kilobots = 0
    frame_number = 0
    speed = 0
    radius = 0
    communication_radius = 0
    arena_center = [0, 0]
    arena_radius = 0
    target_coordinates = [0, 0]
    starting_frame = 0
    pixel_per_m = 0.0
    false_counter_max = 6
    video_name = ""

    def __init__(self, initial_position, kilo_type="lasting"):
        if(Kilobot.speed == 0 or Kilobot.radius == 0):
            print("ERROR: kilobot properties not set")
            exit(-1)

        if(Kilobot.arena_center == [0, 0] or Kilobot.arena_radius == 0):
            print("ERROR: arena properties not set")
            exit(-1)
        self.positions = [initial_position]
        self.current_position = initial_position
        self.max_speed = Kilobot.speed
        self.time = 0
        self.updated = True
        self.update_coef = 1
        self.radius = Kilobot.radius
        self.initial_certainty = 1.0
        self.status = 0
        self.discovery_time = -1
        self.information_time = -1
        self.potential_green = 0
        self.potential_purple = 0
        self.false_purple_counter = 0
        self.false_green_counter = 0
        self.green_validated = 0
        self.possible_next_position = []
        if(kilo_type == "lasting"):
            Kilobot.kilobot_list.append(self)
        elif(kilo_type == "temp"):
            Kilobot.temp_kilobot_list.append(self)
        elif(kilo_type == "target"):
            self.radius *= 1.10
            Kilobot.potential_target_list.append(self)
        else:
            print("Error : wrong type of kilobot entry")
            exit(-1)

    def increase_initial_certainty(self, position):
        self.current_position[0] *= float(self.initial_certainty)
        self.current_position[1] *= float(self.initial_certainty)

        self.initial_certainty += 1
        self.current_position[0] += position[0]
        self.current_position[1] += position[1]

        self.current_position[0] /= float(self.initial_certainty)
        self.current_position[1] /= float(self.initial_certainty)
        self.current_position[0] = int(round(self.current_position[0]))
        self.current_position[1] = int(round(self.current_position[1]))

    def update_position(self, new_position):
        if(self.in_moving_range(new_position)):
            self.positions.append(new_position)
            self.current_position = new_position
            self.updated = True
            self.update_coef = 1
            for i in range(len(self.possible_next_position)):
                temp_kilo = self.possible_next_position[i]
                temp_kilo.possible_next_position.remove(self)
            self.possible_next_position[:] = []
            # if(self.in_communication_range_with_target()):
            # print("status is changing!")
            # self.status = 2
        else:
            print("Asking to update a position out of range!")

    def in_communication_range_with_target(self):
        if(Kilobot.communication_radius == 0):
            print("Error : kilobot paramters not set")
            exit(-1)
        distance = self.distance(Kilobot.target_coordinates)
        if(distance <= Kilobot.communication_radius):
            return True
        return False

    def distance(self, position):
        return math.sqrt(
            (self.current_position[0]-position[0])**2 + (self.current_position[1]-position[1])**2)

    def in_moving_range(self, position):
        displacement = self.distance(position)
        if(displacement <= self.max_speed * self.update_coef):
            return True
        return False

    def in_collision_range(self, position, factor=1.5):
        distance = self.distance(position)
        if(distance <= factor * self.radius):
            return True
        return False

    def _new_frame(self):
        self.updated = False
        self.time += 1

    def is_updated(self):
        return self.updated

    def didnt_find_position(self):
        self.positions.append(self.current_position)
        self.update_coef += 1
        self.updated = True
        self.possible_next_position[:] = []

    def is_closer(self, position, current_closest_kilo, current_min_distance):
        distance = self.distance(position)
        if(distance <= current_min_distance):
            return self, distance
        return current_closest_kilo, current_min_distance

    def get_x(self):
        return self.current_position[0]

    def get_y(self):
        return self.current_position[1]

    def pass_to_green(self):
        self.status = 1
        if(self.information_time == -1):
            self.information_time = Kilobot.frame_number
        self.false_green_counter = 0
        self.discovery_time = -1

    def pass_to_purple(self):
        if(self.in_communication_range_with_target()):
            self.status = 2
            if(self.information_time == -1):
                self.information_time = Kilobot.frame_number
            if(self.discovery_time == -1):
                self.discovery_time = Kilobot.frame_number
            self.false_purple_counter = 0

    def pass_to_neutral(self):
        self.status = 0
        self.discovery_time = -1
        self.information_time = -1
        self.false_purple_counter = 0
        self.false_green_counter = 0

    def on_border(self):
        if self.distance(Kilobot.arena_center) >= 0.9 * Kilobot.arena_radius:
            return True

    @staticmethod
    def find_unupdated_kilobots():
        unupdated_list = []
        for kilo in Kilobot.kilobot_list:
            if(not kilo.is_updated()):
                unupdated_list.append(kilo)
        return unupdated_list

    @staticmethod
    def find_updated_kilobots():
        updated_list = []
        for kilo in Kilobot.kilobot_list:
            if(kilo.is_updated()):
                updated_list.append(kilo)
        return updated_list

    @staticmethod
    def new_frame():
        Kilobot.frame_number += 1
        for kilo in Kilobot.kilobot_list:
            kilo._new_frame()

    @staticmethod
    def get_number_of_kilobots():
        return len(Kilobot.kilobot_list)

    @staticmethod
    def parse_initial_position(position):
        if(not Kilobot.is_a_valid_position(position)):
            return
        # First test if detected position was already taken into account
        for kilo in Kilobot.kilobot_list:
            if(kilo.in_collision_range(position)):
                kilo.increase_initial_certainty(position)
                return

        # Then if not, create a new kilobot instance
        Kilobot(position)

    @staticmethod
    def filter_initial_list(max_num_robots):
        Kilobot.number_of_kilobots = max_num_robots
        if(len(Kilobot.kilobot_list) < max_num_robots):
            print("WARNING : Not enough kilobots were found")
        elif(len(Kilobot.kilobot_list) > max_num_robots):
            print("WARNING : too many kilobots were found on the first image, \
                attempting to remove the false ones")
            Kilobot.remove_kilobots(Kilobot.kilobot_list, len(
                Kilobot.kilobot_list) - max_num_robots)

    @staticmethod
    def remove_kilobots(kilo_list, number_to_remove):
        count = number_to_remove
        while(count != 0):
            lowest_prob = float("inf")
            lowest_kilo = None
            for kilo in kilo_list:
                if(kilo.initial_certainty < lowest_prob):
                    lowest_kilo = kilo
                    lowest_prob = kilo.initial_certainty
            kilo_list.remove(lowest_kilo)
            del lowest_kilo
            count -= 1

    @staticmethod
    def register_position(position):
        if(not Kilobot.is_a_valid_position(position)):
            return
        closest_kilo = None
        mindist = float("inf")
        for kilo in Kilobot.temp_kilobot_list:
            if(kilo.in_collision_range(position, factor=1.2)):
                dist = kilo.distance(position)
                if(dist < mindist):
                    mindist = dist
                    closest_kilo = kilo

        if(closest_kilo):
            closest_kilo.increase_initial_certainty(position)
            return

        # Then if not, create a new kilobot instance
        Kilobot(position, kilo_type="temp")

    @staticmethod
    def compare_certainty(kilo1, kilo2):
        if(kilo1.initial_certainty > kilo2.initial_certainty):
            return -1
        elif(kilo1.initial_certainty < kilo2.initial_certainty):
            return 1
        return 0

    @staticmethod
    def __broken_associate_temp_to_kilobots():
        if(len(Kilobot.temp_kilobot_list) < Kilobot.number_of_kilobots):
            print("WARNING : Not enough kilobots were found in frame %d" %
                  Kilobot.frame_number)
        if(len(Kilobot.kilobot_list) < Kilobot.number_of_kilobots):
            print("len(kilobotlist) = %d" % len(Kilobot.kilobot_list))
        Kilobot.filter_temp_list()

        for kilo in Kilobot.kilobot_list:
            position = kilo.current_position
            # unupdated_list = Kilobot.find_unupdated_kilobots()

            for temp_kilo in Kilobot.temp_kilobot_list:
                if(temp_kilo.in_moving_range(position)):
                    kilo.possible_next_position.append(temp_kilo)
                    temp_kilo.possible_next_position.append(kilo)

        Kilobot.temp_kilobot_list.sort(cmp=Kilobot.compare_certainty)

        for i in range(len(Kilobot.temp_kilobot_list)):
            temp_kilo = Kilobot.temp_kilobot_list[i]
            for j in range(len(temp_kilo.possible_next_position)):
                possible_kilo = temp_kilo.possible_next_position[j]
                if len(possible_kilo.possible_next_position) == 1:
                    if(possible_kilo.is_updated()):
                        print("double catzo")
                    possible_kilo.update_position(temp_kilo.current_position)
                    for k in range(len(temp_kilo.possible_next_position)):
                        linked_kilo = temp_kilo.possible_next_position[k]
                        linked_kilo.possible_next_position.remove(temp_kilo)
                    break
            closest_kilo = None
            dist = float("inf")
            for l in range(len(temp_kilo.possible_next_position)):
                possible_kilo1 = temp_kilo.possible_next_position[l]
                if(not possible_kilo1.is_updated()):
                    (closest_kilo, dist) = possible_kilo1.is_closer(
                        position, closest_kilo, dist)
            if(closest_kilo):
                if(closest_kilo.is_updated()):
                    print("double catzo")
                closest_kilo.update_position(temp_kilo.current_position)
                for n in range(len(temp_kilo.possible_next_position)):
                    linked_kilo = temp_kilo.possible_next_position[n]
                    if(temp_kilo in linked_kilo.possible_next_position):
                        linked_kilo.possible_next_position.remove(temp_kilo)
                    else:
                        print(temp_kilo)
                        print(linked_kilo.possible_next_position)
                        print("catzo")
        unupdated_list = Kilobot.find_unupdated_kilobots()
        if(unupdated_list):
            print("%d unupdated robots at the end of frame %d" %
                  (len(unupdated_list), Kilobot.frame_number))
        for kilo in unupdated_list:
            kilo.didnt_find_position()
        for kilo in Kilobot.temp_kilobot_list:
            del kilo
        Kilobot.temp_kilobot_list[:] = []

    @staticmethod
    def associate_temp_to_kilobots():
        if(len(Kilobot.temp_kilobot_list) < Kilobot.number_of_kilobots):
            print("WARNING : Not enough kilobots were found in frame %d" %
                  Kilobot.frame_number)
        Kilobot.filter_temp_list()
        Kilobot.temp_kilobot_list.sort(cmp=Kilobot.compare_certainty)

        for temp_kilo in Kilobot.temp_kilobot_list:

            position = temp_kilo.current_position
            # unupdated_list = Kilobot.find_unupdated_kilobots()

            closest_kilo = None
            min_distance = float("inf")
            for kilo in Kilobot.kilobot_list:
                if(kilo is None):
                    print("kilo = None!")
                    return
                if(not kilo.is_updated()):
                    (closest_kilo, min_distance) = kilo.is_closer(
                        position, closest_kilo, min_distance)

            if(closest_kilo is not None and closest_kilo.in_moving_range(position)):
                closest_kilo.update_position(position)
        unupdated_list = Kilobot.find_unupdated_kilobots()
        if(unupdated_list):
            print("%d unupdated robots at the end of frame %d" %
                  (len(unupdated_list), Kilobot.frame_number))
        for kilo in unupdated_list:
            kilo.didnt_find_position()
        for kilo in Kilobot.temp_kilobot_list:
            del kilo
        Kilobot.temp_kilobot_list[:] = []

    @staticmethod
    def filter_temp_list():
        couples = []
        list_to_del = []
        for i in range(len(Kilobot.temp_kilobot_list)):
            for j in range(i+1, len(Kilobot.temp_kilobot_list)):
                first_kilo = Kilobot.temp_kilobot_list[i]
                second_kilo = Kilobot.temp_kilobot_list[j]
                if(first_kilo.in_collision_range(second_kilo.current_position)):
                    couples.append((i, j))
        for (i, j) in couples:
            first_kilo = Kilobot.temp_kilobot_list[i]
            second_kilo = Kilobot.temp_kilobot_list[j]
            pos1 = first_kilo.current_position
            pos2 = second_kilo.current_position
            cert1 = first_kilo.initial_certainty
            cert2 = second_kilo.initial_certainty
            first_kilo.current_position[0] = int(
                round(float(pos1[0]*cert1 + pos2[0]*cert2)/(cert1+cert2)))
            first_kilo.current_position[1] = int(
                round(float(pos1[1]*cert1 + pos2[1]*cert2)/(cert1+cert2)))
            first_kilo.initial_certainty = max(cert1, cert2)
            if not second_kilo in list_to_del:
                list_to_del.append(second_kilo)

        for kilo in list_to_del:
            Kilobot.temp_kilobot_list.remove(kilo)

    @staticmethod
    def print_quad_tree():
        for kilo in Kilobot.kilobot_list:
            plt.plot(kilo.get_x(), kilo.get_y(), 'ro')
        plt.gca().invert_yaxis()
        plt.show()

    @staticmethod
    def set_kilobot_param(speed, radius, comm_radius):
        Kilobot.radius = radius
        Kilobot.speed = speed
        Kilobot.communication_radius = comm_radius

    @staticmethod
    def set_arena_param(center, radius, starting_frame, pixel_per_m, video_name):
        Kilobot.arena_radius = radius
        Kilobot.arena_center = center
        Kilobot.starting_frame = starting_frame
        Kilobot.pixel_per_m = pixel_per_m
        Kilobot.video_name = video_name

    @staticmethod
    def is_in_arena(position):
        distance_to_center = int(math.sqrt(math.pow(
            position[0] - Kilobot.arena_center[0], 2) + math.pow(
                position[1] - Kilobot.arena_center[1], 2)))
        if(distance_to_center >= Kilobot.arena_radius):
            return False
        return True

    @staticmethod
    def parse_target_location(position):
        if(not Kilobot.is_in_arena(position)):
            return
        # First test if detected position was already taken into account
        for kilo in Kilobot.potential_target_list:
            if(kilo.in_collision_range(position)):
                kilo.increase_initial_certainty(position)
                return

        # Then if not, create a new kilobot instance
        Kilobot(position, kilo_type="target")

    @staticmethod
    def filter_target_list(number_of_targets):
        if(number_of_targets > 1):
            print("WARNING : code not completely written for multiple targets")
        if(len(Kilobot.potential_target_list) < number_of_targets):
            print("WARNING : Not enough targets were found")
        elif(len(Kilobot.potential_target_list) > number_of_targets):
            print("WARNING : too many targets were found on the first image, \
                attempting to remove the false ones")
            Kilobot.remove_kilobots(Kilobot.potential_target_list,
                                    len(Kilobot.potential_target_list) - number_of_targets)

    @staticmethod
    def compute_target_location():
        if(len(Kilobot.potential_target_list) != 1):
            print("Error : Not a unique target")
            exit()
        Kilobot.target_coordinates = Kilobot.potential_target_list[0].current_position

    @staticmethod
    def target_collision(position):
        if(Kilobot.potential_target_list):
            for target in Kilobot.potential_target_list:
                if target.in_collision_range(position, factor=1.4):
                    return True
            return False
        print("Error: No targets were defined")
        exit(-1)

    @staticmethod
    def is_a_valid_position(position):
        in_arena = Kilobot.is_in_arena(position)
        target_collision = Kilobot.target_collision(position)
        return (in_arena and not target_collision)

    @staticmethod
    def parse_led_position(position, color):
        if(Kilobot.frame_number < Kilobot.starting_frame):
            pass
        elif (Kilobot.is_in_arena(position)):
            r = 1.5 * Kilobot.radius
            mask = [(position[0] + i, position[1] + j)
                    for [i, j] in ([-r, -r], [-r, r], [r, r], [r, -r])]

            for kilo in Kilobot.kilobot_list:
                if(kilo.in_collision_range(position, factor=1.6)):
                    if(color == "green"):
                        kilo.potential_green += 1
                    elif(color == "purple"):
                        kilo.potential_purple += 1

    @staticmethod
    def decide_led_color():
        if(Kilobot.frame_number < Kilobot.starting_frame):
            return
        for kilo in Kilobot.kilobot_list:
            status = kilo.status
            if(kilo.potential_green == 0 and kilo.potential_purple == 0):
                if(not kilo.on_border()):
                    if(status == 1 and not kilo.green_validated):
                        kilo.false_green_counter += 1
                        if(kilo.false_green_counter >= Kilobot.false_counter_max):
                            kilo.pass_to_neutral()
                    elif(status == 2):
                        kilo.false_purple_counter += 1
                        if(kilo.false_purple_counter >= Kilobot.false_counter_max):
                            if(kilo.false_green_counter < -10 or kilo.green_validated):
                                kilo.pass_to_green()
                            else:
                                kilo.pass_to_neutral()

            elif(kilo.potential_purple == 0):
                if(status == 1):
                    kilo.false_green_counter -= 3 * kilo.potential_green
                    if(kilo.false_green_counter < -10):
                        kilo.false_green_counter = - 10000
                        kilo.green_validated = 1
                elif(status == 0):
                    kilo.pass_to_green()
                else:
                    kilo.false_purple_counter += kilo.potential_green
                    if(kilo.false_purple_counter >= Kilobot.false_counter_max):
                        kilo.pass_to_green()

            elif(kilo.potential_green == 0):
                if(status < 2):
                    kilo.pass_to_purple()
                else:
                    kilo.false_purple_counter -= 1 * kilo.potential_purple
                    if(kilo.false_purple_counter < -20):
                        kilo.false_purple_counter = - 100

            else:
                if(status == 2):
                    kilo.false_purple_counter += 1
                    if(kilo.false_purple_counter >= Kilobot.false_counter_max):
                        kilo.pass_to_green()
                elif(status == 0):
                    kilo.pass_to_green()

            # else:
            #     if(status <= 1):
            #         kilo.pass_to_purple()
            #         kilo.false_purple_counter += 1

            kilo.potential_green = 0
            kilo.potential_purple = 0
        return

    @staticmethod
    def to_meter(position):
        return "%.5f, %.5f" % (float(position[0])/Kilobot.pixel_per_m, float(position[1])/Kilobot.pixel_per_m)

    @staticmethod
    def to_meter_disp(distance):
        return "%.5f" % (float(distance)/Kilobot.pixel_per_m)

    @staticmethod
    def finish_experiment():
        date = strftime("%Y%m%d", gmtime())
        date_time = strftime("%Y%m%d-%H:%M:%S", gmtime())
        directory = "real_experiments"
        if not os.path.exists(directory):
            os.makedirs(directory)

        sub_directory = "%s/%s_robots=%d_alpha=%.1f_rho=%.2f_real_expirements" % (
            directory, date, Kilobot.number_of_kilobots, 2.0, 0.90)
        if not os.path.exists(sub_directory):
            os.makedirs(sub_directory)

        file_name = Kilobot.video_name
        sub_sub_directory = "%s/%s" % (sub_directory, file_name)

        if not os.path.exists(sub_sub_directory):
            os.makedirs(sub_sub_directory)

        time_file_name = "%s/%s_time_results.tsv" % (
            sub_sub_directory, date_time)
        position_file_name = "%s/%s_position.tsv" % (
            sub_sub_directory, date_time)
        displacement_file_name = "%s/%s_displacement.tsv" % (
            sub_sub_directory, date_time)
        communication_range_file_name = "%s/%s_comm_range.tsv" % (
            sub_sub_directory, date_time)
        initial_distance_file_name = "%s/%s_initial_distances.tsv" % (
            sub_sub_directory, date_time)
        with open(position_file_name, 'wb') as positions:
            writer = csv.writer(positions, delimiter='\t',
                                quotechar='|', quoting=csv.QUOTE_NONE)
            first_line = ["Robot id"] + ["t = %d" %
                                         i for i in range(0, Kilobot.frame_number - Kilobot.starting_frame - 1)]
            writer.writerow(first_line)
            i = 1

            for kilo in Kilobot.kilobot_list:
                line = [i] + map(Kilobot.to_meter,
                                 kilo.positions[Kilobot.starting_frame:-1])
                writer.writerow(line)
                i += 1
        with open(time_file_name, 'wb') as time_results:
            writer = csv.writer(time_results, delimiter='\t',
                                quotechar='|', quoting=csv.QUOTE_NONE)
            writer.writerow(
                ["Robot id", "First discovery time", "First information time"])
            i = 1

            for kilo in Kilobot.kilobot_list:
                line = [i, max(0, 1 + kilo.discovery_time - Kilobot.starting_frame),
                        max(0, 1 + kilo.information_time - Kilobot.starting_frame)]
                writer.writerow(line)
                i += 1

        with open(displacement_file_name, 'wb') as displacement:
            writer = csv.writer(displacement, delimiter='\t',
                                quotechar='|', quoting=csv.QUOTE_NONE)

            first_line = ["Robot id"] + ["t = %d" %
                                         i for i in range(0, Kilobot.frame_number - Kilobot.starting_frame - 1)]
            writer.writerow(first_line)
            j = 1

            for kilo in Kilobot.kilobot_list:
                kilo.positions = kilo.positions[Kilobot.starting_frame:-1]
                kilo.current_position = kilo.positions[0]
                line = [j] + map(Kilobot.to_meter_disp, [kilo.distance(kilo.positions[i])
                                                         for i in range(len(kilo.positions))])
                writer.writerow(line)
                j += 1

        with open(communication_range_file_name, 'wb') as comm_range:
            writer = csv.writer(comm_range, delimiter='\t',
                                quotechar='|', quoting=csv.QUOTE_NONE)
            line = []
            for kilo in Kilobot.kilobot_list:
                if(kilo.status == 2):
                    kilo.current_position = kilo.positions[kilo.discovery_time -
                                                           Kilobot.starting_frame]
                    distance = kilo.distance(Kilobot.target_coordinates)
                    distance = Kilobot.to_meter_disp(distance)
                    line.append(distance)
            writer.writerow(line)

        with open(initial_distance_file_name, 'wb') as initial_distance:
            writer = csv.writer(initial_distance, delimiter='\t',
                                quotechar='|', quoting=csv.QUOTE_NONE)
            for kilo in Kilobot.kilobot_list:
                line = []
                kilo.current_position = kilo.positions[0]
                distance = kilo.distance(Kilobot.target_coordinates)
                distance = Kilobot.to_meter_disp(distance)
                line.append(distance)
                for other_kilo in Kilobot.kilobot_list:
                    if(other_kilo != kilo):
                        distance = kilo.distance(other_kilo.positions[0])
                        distance = Kilobot.to_meter_disp(distance)
                        line.append(distance)
                writer.writerow(line)
