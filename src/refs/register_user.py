#!/usr/bin/env python
# -*- coding: utf-8 -*-
# lsusb to check device name
#dmesg | grep "tty" to find port name

import serial, time, cv2, face_recognition
from picamera import PiCamera
from picamera.array import PiRGBArray
import numpy as np


class ImageReferenceLoader():
    def __init__(self):
        self.camera = PiCamera()
        self.rawCapture = PiRGBArray(self.camera)
        time.sleep(0.1)

        # Initialize some variables
        self.num_valid = 0
        self.num_req = 10
        self.name = "Aryan"


    def capture_image(self):
        self.camera.capture(self.rawCapture, format="bgr")
        frame = cv2.rotate(self.rawCapture.array, cv2.ROTATE_180)
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Find all the faces and face encodings in the current frame of video
        self.face_locations = face_recognition.face_locations(rgb_small_frame, number_of_times_to_upsample = 2)
        self.face_encodings = face_recognition.face_encodings(rgb_small_frame, self.face_locations)

        if len(self.face_encodings) > 0:
            # See if the face is a match for the known face(s)
            np.savetxt(self.name + 'encoding' + str(self.num_valid) + '.txt', self.face_encodings[0])
            self.num_valid += 1

        self.rawCapture.truncate()
        self.rawCapture.seek(0)

        return str(self.num_valid)


if __name__ == '__main__':
    irl = ImageReferenceLoader()
    print('Running. Press CTRL-C to exit.')
    with serial.Serial("/dev/ttyACM0", 9600, timeout=1) as arduino:
        time.sleep(0.1) #wait for serial to open
        if arduino.isOpen():
            arduino.flush()
            print("{} connected!".format(arduino.port))
            try:
                while irl.num_valid < irl.num_req:
                    arduino.flush()
                    output = irl.capture_image()
                    arduino.write(output.encode())
                    time.sleep(0.1)

            except KeyboardInterrupt:
                print("KeyboardInterrupt has been caught.")
