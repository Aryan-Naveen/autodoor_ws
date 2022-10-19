#!/bin/bash

arduino-cli compile --fqbn arduino:avr:uno arduino_doorctrl/
arduino-cli upload --port /dev/ttyACM0 arduino_doorctrl/
