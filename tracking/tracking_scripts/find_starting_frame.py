import cv2
import argparse
import os
from kilobot_tracking import X1, X2, Y1, Y2, arena_center, arena_radius


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--video", default="",
                    help="path to the (optional) video file")
    ap.add_argument("-f", "--folder", default="",
                    help="path to a folder")

    args = vars(ap.parse_args())

    video = args["video"]
    folder = args["folder"]

    if(video):
        find_first_frame(video)

    elif(folder):
        for video in os.listdir(folder):
            if(video.endswith(".MP4")):
                find_first_frame(video, folder=folder)


def find_first_frame(video, folder=""):
    complete_file_name = video
    if(folder):
        complete_file_name = "%s/%s" % (folder, complete_file_name)

    restart = True
    while restart:
        restart = False
        camera = cv2.VideoCapture(complete_file_name)
        camera.set(cv2.CAP_PROP_FPS, 29)
        print("Opening video %s" % video)
        frame_counter = 0
        x_offset = 0
        y_offset = 0
        r_offset = 0
        while True:
            # grab the current frame
            (grabbed, frame) = camera.read()
            if grabbed:
                frame_2 = (frame[Y1+y_offset:Y2 +
                                 y_offset, X1+x_offset:X2+x_offset]).copy()
                fontColor = (0, 0, 255)
                upper_right_corner = (100, 200)
                font = cv2.FONT_HERSHEY_SIMPLEX
                fontScale = 5
                lineType = 2
                cv2.putText(frame_2, "%d" % frame_counter,
                            upper_right_corner,
                            font,
                            fontScale,
                            fontColor,
                            lineType)
                cv2.circle(frame_2, tuple(arena_center),
                           arena_radius + r_offset, (255, 255, 100), 2)
                cv2.imshow("Frame", frame_2)
                key = cv2.waitKey(1000) & 0xFF
                # if the 'q' key is pressed, stop the loop
                if key == ord("q"):
                    break
                if key == ord("p"):
                    print("Frame %d selected. Confirm? (y/n/r)" %
                          frame_counter)
                    finished = False
                    while(True):
                        key = cv2.waitKey(1000) & 0xFF
                        if key == ord("y"):
                            print("\tConfirmed")
                            create_config(
                                complete_file_name, frame_counter, x_offset, y_offset, r_offset)
                            finished = True
                            break
                        elif key == ord("n"):
                            print("\tCanceled, resuming")
                            break
                        elif key == ord("r"):
                            print("\tReturning to the beginning")
                            restart = True
                            finished = True
                            break
                        else:
                            if key == 180:
                                x_offset -= 1
                            elif key == 182:
                                x_offset += 1
                            elif key == 184:
                                y_offset -= 1
                            elif key == 178:
                                y_offset += 1
                            elif key == 171:
                                r_offset += 1
                            elif key == 173:
                                r_offset -= 1
                            frame_3 = frame[Y1+y_offset:Y2 +
                                            y_offset, X1+x_offset:X2+x_offset].copy()
                            fontColor = (0, 0, 255)
                            upper_right_corner = (100, 200)
                            font = cv2.FONT_HERSHEY_SIMPLEX
                            fontScale = 5
                            lineType = 2
                            cv2.putText(frame_3, "%d" % frame_counter,
                                        upper_right_corner,
                                        font,
                                        fontScale,
                                        fontColor,
                                        lineType)
                            cv2.circle(frame_3, tuple(arena_center),
                                       arena_radius + r_offset, (255, 255, 100), 2)
                            cv2.imshow("Frame", frame_3)
                    if finished:
                        break
                frame_counter += 1


def create_config(pathname, frame_number, x_offset, y_offset, r_offset):
    new_path_name = pathname.split(".")[0] + ".txt"
    f = open(new_path_name, "w+")
    f.write("%d\n%d\n%d\n%d" % (frame_number, x_offset, y_offset, r_offset))
    f.close()


if __name__ == "__main__":
    main()
