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
    rawCapture = PiRGBArray(self.camera)
    while num_valid < req_valid:
        camera.capture(self.rawCapture, format="bgr")
        frame = cv2.rotate(self.rawCapture.array, cv2.ROTATE_180)
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Find all the faces and face encodings in the current frame of video
        self.face_locations = face_recognition.face_locations(rgb_small_frame, number_of_times_to_upsample = 2)
        self.face_encodings = face_recognition.face_encodings(rgb_small_frame, self.face_locations)
        if len(face_encodings) > 0:
            print(face_encodings[0])
            req_valid += 1

            print(req_valid)
