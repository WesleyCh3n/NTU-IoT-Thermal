#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import cmapy
import cv2
import h5py
import numpy as np
import pathlib
import time

from datetime import datetime, timedelta
from queue import Queue

from uvctypes import *

BUF_SIZE = 3
q = Queue(BUF_SIZE)

parser = argparse.ArgumentParser()
parser.add_argument("-s", action="store_true", help="save img")
parser.add_argument("-v", action="store_true", help="show img")
args = parser.parse_args()
if args.s:
    print(f"saving hdf5")


def py_frame_callback(frame, userptr):
    array_pointer = cast(frame.contents.data, POINTER(c_uint16 * (frame.contents.width * frame.contents.height)))
    data = np.frombuffer(
        array_pointer.contents, dtype=np.dtype(np.uint16)
    ).reshape(
        frame.contents.height, frame.contents.width
    )

    if frame.contents.data_bytes != (2 * frame.contents.width * frame.contents.height):
        return

    if not q.full():
        q.put(data)

PTR_PY_FRAME_CALLBACK = CFUNCTYPE(None, POINTER(uvc_frame), c_void_p)(py_frame_callback)

def therPre(raw_ther, shape):
    ther_img = (raw_ther - 27315)/100.0
    ther_img = 255*(ther_img - ther_img.min())/(ther_img.max()-ther_img.min())
    ther_img = cv2.applyColorMap(ther_img.astype(np.uint8), cmapy.cmap('RdGy_r'))
    ther_img = cv2.resize(ther_img, shape)
    return ther_img

def main():
    # Flir preparation
    ctx = POINTER(uvc_context)()
    dev = POINTER(uvc_device)()
    devh = POINTER(uvc_device_handle)()
    ctrl = uvc_stream_ctrl()
    if libuvc.uvc_init(byref(ctx), 0) < 0:
        print("uvc_init error")
        exit(1)
    if libuvc.uvc_find_device(ctx, byref(dev), PT_USB_VID, PT_USB_PID, 0) < 0:
        print("uvc_find_device error")
        exit(1)
    if libuvc.uvc_open(dev, byref(devh)) < 0:
        print("uvc_open error")
        exit(1)

    print("device opened!")
    print_device_info(devh)
    print_device_formats(devh)
    frame_formats = uvc_get_frame_formats_by_guid(devh, VS_FMT_GUID_Y16)
    if len(frame_formats) == 0:
        print("device does not support Y16")
        exit(1)
    libuvc.uvc_get_stream_ctrl_format_size(devh, byref(ctrl), UVC_FRAME_FORMAT_Y16,
        frame_formats[0].wWidth, frame_formats[0].wHeight, int(1e7 / frame_formats[0].dwDefaultFrameInterval)
    )
    if libuvc.uvc_start_streaming(devh, byref(ctrl), PTR_PY_FRAME_CALLBACK, None, 0) < 0:
        print("uvc_start_streaming failed: {0}".format(res))
        exit(1)

    if args.s:
        start_time = datetime.now()
        timestr = start_time.strftime('%Y%m%d-%H%M%S')
        hdf5_file = h5py.File(f'IR_HDF5_{timestr}.HDF5', mode='w')
        frame = 1
    while True:
        data = q.get(True, 500)
        if data is None:
            break

        if args.s:
            key_time = datetime.now()
            hdf5_file.create_dataset((key_time.strftime('%H%M%S.%f')), data=data)
            frame += 1
            if (key_time-start_time) > timedelta(minutes=5):
                break

        if args.v:
            cv2.imshow('Lepton Radiometry', therPre(data, (320,240)))
        if cv2.waitKey(20) == 27:
            break

    if args.s:
        hdf5_file.close()
    cv2.destroyAllWindows()
    libuvc.uvc_stop_streaming(devh)
    libuvc.uvc_unref_device(dev)
    libuvc.uvc_exit(ctx)
    print("done")

if __name__ == '__main__':
    main()
