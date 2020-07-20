import cv2
import numpy as np
import os
import argparse
from os.path import isfile, join


def parse_args():
    parser = argparse.ArgumentParser(
        description='Convert frames to video')

    parser.add_argument('--image_path', type=str,
                        help='path to a test image or folder of images', required=True)

    parser.add_argument('--output_name', type=str,
                        help='path to pose output of the model', required=True)

    return parser.parse_args()

# the input image format better be png
def convert_frames_to_video(args):
    frame_array = []
    files = [f for f in os.listdir(args.image_path) if isfile(join(args.image_path, f))]

    #for sorting the file names properly
    files.sort()


    for i in range(len(files)):
        filename = args.image_path + files[i]

        if files[i] == '.DS_Store':
            continue

        #reading each files
        img = cv2.imread(filename)

        height, width, layers = img.shape
        size = (width,height)
        # print(filename)
        #inserting the frames into an image array
        frame_array.append(img)

    out = cv2.VideoWriter(args.output_name, cv2.VideoWriter_fourcc(*'mp4v'), 10.0, size)

    for i in range(len(frame_array)):
        # writing to a image array
        out.write(frame_array[i])
    out.release()
    print("Video successfully generated")

if __name__=="__main__":
    args = parse_args()
    convert_frames_to_video(args)
