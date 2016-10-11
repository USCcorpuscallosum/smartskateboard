#!/usr/bin/python

# Installation:
# sudo apt-get update
# sudo apt-get install sense-hat
# sudo reboot

# Disclaimer: I don't know if this even compiles...
# TODO
# - what if they are going in the other direction?
# - fade in to color
# - wipe forward/backward with color - like audi

import time
from sense_hat import SenseHat

sense = SenseHat()

# Which direction is forward
FORWARD_VEC = {'x': 0, 'y': 0, 'z': 1}

# If the acceleration is greater than this, show a color
ACCELERATION_THRESHOLD = 0

FORWARD_COLOR = [0, 255, 0]
BACKWARD_COLOR = [255, 0, 0]

msleep = lambda x: time.sleep(x / 1000.0)

def dot(vec1, vec2):
    return vec1['x'] * vec2['x'] + vec1['y'] * vec2['y'] + vec1['z'] * vec2['z']

def get_forward_acceleration():
    raw = sense.get_accelerometer_raw()
    # print("x: {x}, y: {y}, z: {z}".format(**raw))

    return dot(raw, FORWARD_VEC)

while True:
    acc = get_forward_acceleration()
    if acc > ACCELERATION_THRESHOLD:
        sense.clear(FORWARD_COLOR)
    elif acc < -ACCELERATION_THRESHOLD:
        sense.clear(BACKWARD_COLOR)
    else:
        sense.clear([0, 0, 0])

    msleep(2)
