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
        show_first_and_last_frame(video)

    elif(folder):
        for video in os.listdir(folder):
            if(video.endswith(".MP4")):
                show_first_and_last_frame(video, folder=folder)


def show_first_and_last_frame(video, folder=""):
    complete_file_name = video
    if(folder):
        complete_file_name = "%s/%s" % (folder, complete_file_name)

    camera = cv2.VideoCapture(complete_file_name)
    camera.set(cv2.CAP_PROP_FPS, 29)
    print("Opening video %s" % video)
    frame_counter = 0
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


if __name__ == "__main__":
    main()
