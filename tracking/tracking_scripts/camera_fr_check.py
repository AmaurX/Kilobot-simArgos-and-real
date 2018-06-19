import cv2
import argparse
import os


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

    camera = cv2.VideoCapture(complete_file_name)
    camera.set(cv2.CAP_PROP_FPS, 29)
    print("Opening video %s" % video)
    frame_counter = 0
    x_offset = 0
    y_offset = 0
    r_offset = 0
    old_frame = None
    while True:
        # grab the current frame
        (grabbed, frame) = camera.read()
        if grabbed:
            fontColor = (0, 0, 255)
            upper_right_corner = (100, 200)
            font = cv2.FONT_HERSHEY_SIMPLEX
            fontScale = 5
            lineType = 2
            cv2.putText(frame, "%d" % frame_counter,
                        upper_right_corner,
                        font,
                        fontScale,
                        fontColor,
                        lineType)
            if(frame_counter == 0):
                cv2.imshow("Frame", frame)
                key = cv2.waitKey(5000) & 0xFF
            frame_counter += 1
            old_frame = frame
        else:
            cv2.imshow("Frame", old_frame)
            key = cv2.waitKey(5000) & 0xFF
            break


def create_config(pathname, frame_number, x_offset, y_offset, r_offset):
    new_path_name = pathname.split(".")[0] + ".txt"
    f = open(new_path_name, "w+")
    f.write("%d\n%d\n%d\n%d" % (frame_number, x_offset, y_offset, r_offset))
    f.close()


if __name__ == "__main__":
    main()
