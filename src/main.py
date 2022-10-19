#!/usr/bin/env python
# -*- coding: utf-8 -*-
# lsusb to check device name
#dmesg | grep "tty" to find port name

import serial, time, cv2, face_recognition
from picamera import PiCamera
from picamera.array import PiRGBArray
import numpy as np

class Validator():
    def __init__(self):
        self.camera = PiCamera()
        self.rawCapture = PiRGBArray(self.camera)
        time.sleep(0.1)

        # Initialize some variables
        self.initialize_roomate_encodings()
        self.face_locations = []
        self.face_encodings = []
        self.face_names = []


    def initialize_roomate_encodings(self):
        # aryan_image = cv2.rotate(face_recognition.load_image_file("refs/aryan.jpg"), cv2.ROTATE_180)
        # aryan_face_encoding = face_recognition.face_encodings(aryan_image)[0]
        aryan_face_encoding = np.loadtxt('refs/aryan_encoding.txt')

        # Create arrays of known face encodings and their names
        self.known_face_encodings = [
            aryan_face_encoding
        ]
        self.known_face_names = [
            "Aryan Naveen"
        ]



    def validate_person(self):
        self.camera.capture(self.rawCapture, format="bgr")
        frame = cv2.rotate(self.rawCapture.array, cv2.ROTATE_180)
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Find all the faces and face encodings in the current frame of video
        self.face_locations = face_recognition.face_locations(rgb_small_frame, number_of_times_to_upsample = 2)
        self.face_encodings = face_recognition.face_encodings(rgb_small_frame, self.face_locations)

        face_names = []
        print(len(self.face_encodings))
        for face_encoding in self.face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
            name = "Unknown"

            # # If a match was found in known_face_encodings, just use the first one.
            # if True in matches:
            #     first_match_index = matches.index(True)
            #     name = known_face_names[first_match_index]

            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = self.known_face_names[best_match_index]

            face_names.append(name)

        print(face_names)
        self.rawCapture.truncate()
        self.rawCapture.seek(0)
        if len(face_names) > 0 and face_names[0] in self.known_face_names:
            return face_names[0]
        else:
            return "-1"

if __name__ == '__main__':
    validate = Validator()
    print('Running. Press CTRL-C to exit.')
    with serial.Serial("/dev/ttyACM0", 9600, timeout=1) as arduino:
        time.sleep(0.1) #wait for serial to open
        if arduino.isOpen():
            arduino.flush()
            print("{} connected!".format(arduino.port))
            try:
                while True:
                    while arduino.inWaiting() == 0: pass
                    arduino.flushInput()
                    print("Activated")
                    output = validate.validate_person()
                    arduino.write(output.encode())

            except KeyboardInterrupt:
                print("KeyboardInterrupt has been caught.")
