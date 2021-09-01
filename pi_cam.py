import argparse
import cv2
import numpy as np
import pathlib
import time

from picamera import PiCamera
from datetime import datetime, timedelta

parser = argparse.ArgumentParser()
parser.add_argument("-s", action="store_true", help="save img")
parser.add_argument("-v", action="store_true", help="show img")
args = parser.parse_args()

img_dir = 'rgb_img'
# size = (1280, 960)
size = (1600, 1200)

start_time = datetime.now()
if args.s:
    print(f"saving image to {img_dir}")

with PiCamera() as camera:
    # Setting up camera
    camera.resolution = size
    camera.start_preview()
    buff = np.empty((size[1], size[0], 3), dtype=np.uint8)
    stream = camera.capture_continuous(buff, format='bgr')
    for img in stream:
        key_time = datetime.now()
        datestr = key_time.strftime("%Y_%m_%d")

        pathlib.Path(f'{img_dir}/{datestr}').mkdir(parents=True, exist_ok=True)
        timestr = key_time.strftime("%Y%m%d-%H%M%S")
        if args.s:
            if (key_time-start_time) > timedelta(minutes=5, seconds=10):
                break
            cv2.imwrite(f'{img_dir}/{datestr}/{timestr}.jpg', buff)
            print(f'{img_dir}/{datestr}/{timestr}.jpg save')
        if args.v:
            cv2.imshow('PiCam', cv2.resize(buff, (320,240)))
        if cv2.waitKey(20) == 27:
            break
    camera.stop_preview()
