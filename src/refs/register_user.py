#!/usr/bin/env python
# -*- coding: utf-8 -*-
# lsusb to check device name
#dmesg | grep "tty" to find port name

import serial, time, cv2, face_recognition
from picamera import PiCamera
from picamera.array import PiRGBArray
import numpy as np

if __name__ == '__main__':
    name = "Aryan"
    num_valid = 0
    req_valid = 1
    camera = PiCamera()
    rawCapture = PiRGBArray(camera)
    time.sleep(0.1)
    print("starting")
    while num_valid < req_valid:
        camera.capture(rawCapture, format="bgr")
        frame = cv2.rotate(rawCapture.array, cv2.ROTATE_180)
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame, number_of_times_to_upsample = 2)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        if len(face_encodings) > 0:
            print(face_encodings[0])
            req_valid += 1

            print(req_valid)
        else:
            print('invalid')
        rawCapture.truncate()
        rawCapture.seek(0)
