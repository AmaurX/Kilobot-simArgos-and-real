# import the necessary packages
import argparse
import os
from collections import deque
from time import gmtime, strftime

import numpy as np

import cv2
import imutils
from kilobot import Kilobot

kilobot_radius = 16
# Should be around 9.1 * speed/frame, which means 5 pixel/frame ....
kilobot_speed = 17
arena_center = [460, 460]
arena_radius = 430
colors = [(255, 120, 0), (120, 255, 120), (255, 0, 255), (0, 255, 0),
          (255, 0, 0), (255, 150, 80)]
communication_radius = 250

kilobot_threshold = 0.465
led_threshold = 0.75
target_threshold = 0.70

D = 920
Y1 = 80
Y2 = Y1 + D
X1 = 565
X2 = X1 + D


# in RGB!
green_min = [70, 210, 70]
green_max = [255, 255, 210]

purple_min = [245, 110, 238]
purple_max = [255, 247, 255]

# grey_min = [28, 109, 81]
# grey_max = [155, 153, 164]
grey_min = [45, 65, 45]
grey_max = [170, 155, 170]


def is_of_color(color_str, (blue, green, red)):
    if(color_str == "purple"):
        mini = red >= purple_min[0] and green >= purple_min[1] and blue >= purple_min[2]
        maxi = red <= purple_max[0] and green <= purple_max[1] and blue <= purple_max[2]
        if(mini and maxi):
            return True
        return False

    elif(color_str == "green"):
        mini = red >= green_min[0] and green >= green_min[1] and blue >= green_min[2]
        maxi = red <= green_max[0] and green <= green_max[1] and blue <= green_max[2]
        if(mini and maxi):
            return True
        return False

    elif(color_str == "grey"):
        mini = red >= grey_min[0] and green >= grey_min[1] and blue >= grey_min[2]
        maxi = red <= grey_max[0] and green <= grey_max[1] and blue <= grey_max[2]
        if(mini and maxi):
            return True
        return False


def main():
    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--video",
                    help="path to the (optional) video file")
    ap.add_argument("-b", "--buffer", type=int, default=64,
                    help="max buffer size")
    ap.add_argument("-s", "--starting_frame", type=int, default=3,
                    help="visualize result during processing (default = 1)")
    ap.add_argument("-i", "--visualization", type=int, default=1,
                    help="visualize result during processing (default = 1)")
    ap.add_argument("-n", "--numberOfRobots",
                    help="number of robots to find in the image (not counting the target)", type=int, default=30)

    ap.add_argument("-x", "--x_offset",
                    help="number of pixel to offset x (from the left)", type=int, default=0)
    ap.add_argument("-y", "--y_offset",
                    help="number of pixel to offset y (from the top)", type=int, default=0)
    ap.add_argument("-r", "--r_offset",
                    help="number of pixel to offset the radius", type=int, default=0)
    args = vars(ap.parse_args())

    numberOfRobots = args["numberOfRobots"]
    visualization = args["visualization"]
    starting_frame = args["starting_frame"]
    x_offset = args["x_offset"]
    y_offset = args["y_offset"]
    r_offset = args["r_offset"]
    print(args["video"])

    if os.path.isfile(args["video"].split(".")[0]+".txt"):
        f = open(args["video"].split(".")[0]+".txt", 'r')
        metadata = f.readlines()
        starting_frame = int(metadata[0])
        x_offset += int(metadata[1])
        y_offset += int(metadata[2])
        r_offset += int(metadata[3])

    global X1, X2, Y1, Y2, arena_radius
    X1 += x_offset
    X2 += x_offset
    Y1 += y_offset
    Y2 += y_offset
    arena_radius += r_offset
    result_video_folder = args["video"].split(
        '/')[0] + "/treated_videos/" + args["video"].split('/')[2] + "/"
    if not os.path.exists(result_video_folder):
        os.mkdir(result_video_folder)
    out = cv2.VideoWriter(result_video_folder + args["video"].split('/')[-1].split('.')[0] + "_out.avi", cv2.VideoWriter_fourcc(
        'M', 'J', 'P', 'G'), 10.0, (X2-X1, Y2-Y1))
    # Set parameters for the kilobot class and the arena

    ten_cm_template = "tracking/templates/10cm_templates/10cm.png"
    template = cv2.imread(ten_cm_template, 0)
    w, h = template.shape[::-1]
    pixel_per_m = float(w) / 0.10
    # print(pixel_per_m)

    print(starting_frame)
    Kilobot.set_kilobot_param(
        kilobot_speed, kilobot_radius, communication_radius)
    Kilobot.set_arena_param(arena_center, arena_radius,
                            starting_frame, pixel_per_m, args["video"].split('/')[-1].split('.')[0])

    # if a video path was not supplied, grab the reference
    # to the webcam
    if not args.get("video", False):
        camera = cv2.VideoCapture(0)

    # otherwise, grab a reference to the video file
    else:
        camera = cv2.VideoCapture(args["video"])
        camera.set(cv2.CAP_PROP_FPS, 29)

    # keep looping
    is_first_frame = True
    first_bug = True
    frame_counter = 0
    missing_frame_counter = 0

    while True:
        # grab the current frame
        (grabbed, frame) = camera.read()

        # if we are viewing a video and we did not grab a frame,
        # then we have reached the end of the video, or there is a missing frame

        if args.get("video") and not grabbed:
            if(missing_frame_counter < 10):
                missing_frame_counter += 1
                continue
            else:
                print("End of video file ?")
                date = strftime("%Y%m%d", gmtime())

                folder = "%s_robots=%d_alpha=%.1f_rho=%.2f_real_expirements" % (
                    date, Kilobot.number_of_kilobots, 2.0, 0.90)
                Kilobot.finish_experiment(folder)
                break
        else:
            if(first_bug == False):
                print("Warning : Missing frame")
            missing_frame_counter = 0
        # crop to the arena
        # Arena is in rectangle x,y,w,h = 570, 50, 930, 910
        # cv2.rectangle(frame, (570, 50), (1500, 960), (255, 255, 0), 2) WORKS WITH UNCROPPED IMAGE
        frame = frame[Y1:Y2, X1:X2]  # Y1:Y2 , X1:X2
        img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame_copy = frame.copy()
        # Do a multiple template matching to find the target
        if(is_first_frame):
            folder = "tracking/templates/target_templates/"
            for template_name in os.listdir(folder):
                template = cv2.imread(folder + template_name, 0)
                w, h = template.shape[::-1]
                res = cv2.matchTemplate(
                    img_gray, template, cv2.TM_CCOEFF_NORMED)
                threshold = target_threshold
                loc = np.where(res >= threshold)
                for (x, y) in zip(*loc[::-1]):
                    Kilobot.parse_target_location([x+w/2, y+h/2])
                    # cv2.circle(frame, (x+w/2, y+h/2), w/2, (255, 0, 255), 2)
                    # cv2.circle(frame, (x+w/2, y+h/2), 2, (0, 0, 255), 2)

            Kilobot.filter_target_list(1)
            Kilobot.compute_target_location()

        # Show the target in red
        for kilo in Kilobot.potential_target_list:
            # cv2.circle(frame, (kilo.current_position[0],
            #                    kilo.current_position[1]), int(kilobot_radius * 1.60), (255, 0, 0), 2)
            cv2.circle(frame, (kilo.current_position[0],
                               kilo.current_position[1]), communication_radius, colors[2], 1)

        # Do a multiple template matching, to take the rotation and angle of view into account
        folder = "tracking/templates/kilobot_templates/"
        for template_name in os.listdir(folder):
            template = cv2.imread(folder + template_name, 0)
            w, h = template.shape[::-1]
            res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
            threshold = kilobot_threshold
            loc = np.where(res >= threshold)
            for (x, y) in zip(*loc[::-1]):
                if(is_first_frame):
                    Kilobot.parse_initial_position([x+w/2, y+h/2])
                else:
                    Kilobot.register_position([x+w/2, y+h/2])
            # cv2.circle(frame, (x+w/2, y+h/2),
            #            16, (255, 0, 255), 2)

        font = cv2.FONT_HERSHEY_SIMPLEX

        fontScale = 0.5
        lineType = 2

        # Take n robots only on the first frame
        if(is_first_frame):
            print("number of registered kilobots before filter = %d" %
                  Kilobot.get_number_of_kilobots())
            Kilobot.filter_initial_list(numberOfRobots)
            print("number of registered kilobots after filter = %d" %
                  Kilobot.get_number_of_kilobots())

        # Associate temp kilobots position to lasting ones by proximity
        else:
            list_to_remove = []
            for kilo in Kilobot.temp_kilobot_list:
                grey_counter = 0
                counter = 0
                [x, y] = kilo.current_position
                r = kilo.radius
                for i in range(-r/2, r/2):
                    for j in range(-r/2, r/2):
                        if(i*i + j*j <= r*r):
                            counter += 1
                            blue = frame_copy.item(y + j, x + i, 0)
                            green = frame_copy.item(y + j, x + i, 1)
                            red = frame_copy.item(y + j, x + i, 2)
                            if(is_of_color("grey", (blue, green, red)) and not is_of_color("green", (blue, green, red)) and not is_of_color("purple", (blue, green, red))):
                                grey_counter += 1
                grey_proportion = float(grey_counter)/float(counter)

                if(grey_proportion > 0.60):
                    # kilo.initial_certainty = int(
                    #     round(kilo.initial_certainty / (20.0 * grey_proportion)))
                    # cv2.circle(frame, (kilo.current_position[0],
                    #                    kilo.current_position[1]), 5, (255, 255, 120), 2)
                    list_to_remove.append(kilo)
                elif(grey_proportion > 0.30):
                    kilo.initial_certainty = int(round(kilo.initial_certainty /
                                                       (10.0 * (grey_proportion - 0.20))))

                # bottomLeftCornerOfText = (x+w/2, y+h/2)
                # cv2.putText(frame, "%.2f" % grey_proportion,
                #             bottomLeftCornerOfText,
                #             font,
                #             fontScale,
                #             (0, 0, 0),
                #             lineType)
        # Show the temporary detected kilobots in purple, before assignement to Kilobot lasting entities
            for kilo in list_to_remove:
                Kilobot.temp_kilobot_list.remove(kilo)
                del kilo
            # for kilo in Kilobot.temp_kilobot_list:
            #     cv2.circle(frame, (kilo.current_position[0],
            #                        kilo.current_position[1]), kilobot_radius, (120, 0, 120), max(1, int(round(0.05 * kilo.initial_certainty))))

            Kilobot.associate_temp_to_kilobots()

        # Do a multiple template matching, to take the rotation and angle of view into account
        folder = "tracking/templates/led_templates/"
        for template_name in os.listdir(folder):
            template = cv2.imread(folder + template_name, 0)
            w, h = template.shape[::-1]
            res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
            threshold = led_threshold
            loc = np.where(res >= threshold)
            for (x, y) in zip(*loc[::-1]):
                # if(is_first_frame):
                    # Kilobot.parse_initial_position([x+w/2, y+h/2])
                # else:
                    # Kilobot.register_position([x+w/2, y+h/2])
                # cv2.circle(frame, (x+w/2, y+h/2), 5, (255, 0, 255), 1)
                counter_purple = 0
                counter_green = 0
                counter = 0
                color = [0, 0, 0]  # (BGR)
                for i in range(-w/2, w/2):
                    for j in range(-h/2, h/2):
                        counter += 1
                        if(i*i + j*j <= w*h):
                            blue = frame_copy.item(y+h/2 + j, x + w/2 + i, 0)
                            green = frame_copy.item(y+h/2 + j, x + w/2 + i, 1)
                            red = frame_copy.item(y+h/2 + j, x + w/2 + i, 2)
                            if(is_of_color("purple", (blue, green, red))):
                                counter_purple += 1
                            if(is_of_color("green", (blue, green, red))):
                                counter_green += 1

                text = "green = %d; purple = %d" % (
                    counter_green, counter_purple)
                fontColor = (0, 0, 0)
                if(0.0 < float(counter_green)/counter < 0.05 and float(counter_purple)/counter < 0.05):
                    # not enough color to be sure
                    # cv2.circle(
                    #     frame, (x+w/2, y+h/2), 15, fontColor, 1)
                    continue
                elif(counter_green > counter_purple):
                    fontColor = (0, 255, 0)
                    # cv2.circle(frame, (x+w/2, y+h/2), 15, fontColor, 1)
                    Kilobot.parse_led_position((x+w/2, y+h/2), "green")
                elif(counter_green < counter_purple):
                    fontColor = (255, 0, 255)
                    # cv2.circle(frame, (x+w/2, y+h/2), 15, fontColor, 1)
                    Kilobot.parse_led_position((x+w/2, y+h/2), "purple")

                # bottomLeftCornerOfText = (x+w/2, y+h/2)
                # cv2.putText(frame, text,
                #             bottomLeftCornerOfText,
                #             font,
                #             fontScale,
                #             fontColor,
                #             lineType)

        Kilobot.decide_led_color()
        # Draw circles around lasting kilobots
        for kilo in Kilobot.kilobot_list:
            status = kilo.status
            certainty = 0
            if(status == 1 and kilo.false_green_counter < -10):
                certainty = 2
            if(status == 2 and kilo.false_purple_counter < -20):
                certainty = 2

            cv2.circle(frame, (kilo.current_position[0],
                               kilo.current_position[1]), kilobot_radius, colors[status], max(2, 3 + certainty - kilo.update_coef))
            if(status == 2):
                cv2.circle(frame, (kilo.purple_led_position[0],
                                   kilo.purple_led_position[1]), 2, colors[status+2], 2)
            if(status == 1):
                cv2.circle(frame, (kilo.green_led_position[0],
                                   kilo.green_led_position[1]), 2, colors[5], 2)
            # if(status > 0):
            #     cv2.circle(frame, (kilo.current_position[0],
            #                        kilo.current_position[1]), communication_radius, colors[1], 1)

        # Draw arena circle, to make sure it is ajusted
        cv2.circle(frame, tuple(arena_center),
                   arena_radius, (255, 255, 100), 2)
        cv2.circle(frame, tuple(arena_center),
                   int(0.9 * arena_radius), (255, 255, 100), 1)
        fontColor = (0, 0, 0)
        upper_right_corner = (10, 20)
        cv2.putText(frame, "%d" % frame_counter,
                    upper_right_corner,
                    font,
                    fontScale,
                    fontColor,
                    lineType)

        # Write the image into the result video
        out.write(frame)
        # frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # cv2.imwrite("res.png", frame)

        # Show image if asked
        if(visualization == True):
            cv2.imshow("Frame", frame)

        key = cv2.waitKey(1) & 0xFF
        is_first_frame = False
        Kilobot.new_frame()
        # if the 'q' key is pressed, stop the loop
        if key == ord("q"):
            date = strftime("%Y%m%d", gmtime())
            folder = "%s_robots=%d_alpha=%.1f_rho=%.2f_real_expirements" % (
                date, Kilobot.number_of_kilobots, 2.0, 0.90)
            Kilobot.finish_experiment(folder)

            break
        if key == ord("p"):
            print("INFO : paused")
            while(True):
                key = cv2.waitKey(10) & 0xFF
                if key == ord("u"):
                    print("INFO : resumed")
                    break
        frame_counter += 1
    # cleanup the camera and close any open windows
    camera.release()
    out.release()
    cv2.destroyAllWindows()


def find_enclosing_rectangle(img_gray, frame):
    template_board = cv2.imread("board.png", 0)
    # gray_template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    w, h = template_board.shape[::-1]
    res = cv2.matchTemplate(img_gray, template_board, cv2.TM_CCOEFF_NORMED)
    threshold = 0.35
    loc = np.where(res >= threshold)
    for (x, y) in zip(*loc[::-1]):
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 255, 0), 2)
        print("x = %d, y = %d, w = %d, h = %d" % (x, y, w, h))


if __name__ == "__main__":
    main()
