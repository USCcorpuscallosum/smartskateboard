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

# https://learn.adafruit.com/neopixels-on-raspberry-pi/overview
# https://github.com/jgarff/rpi_ws281x
# http://abyz.co.uk/rpi/pigpio/python.html
# https://wiki.qt.io/Apt-get_Qt4_on_the_Raspberry_Pi

import time
from sense_hat import SenseHat

sense = SenseHat()

# Which direction is forward
FORWARD_VEC = {'x': 0, 'y': 0, 'z': 1}

# If the acceleration is greater than this, show a color
ACCELERATION_THRESHOLD = 0
# We could create individual variables for the three RGB variables that change at different rates and use inside the color functions
# That way we could have unique color combinations according to not only acceleration, but also direction
FORWARD_COLOR = [0, 255, 0]
BACKWARD_COLOR = [255, 0, 0]

msleep = lambda x: time.sleep(x / 1000.0)

def dot(vec1, vec2):
    return vec1['x'] * vec2['x'] + vec1['y'] * vec2['y'] + vec1['z'] * vec2['z']

def lerp(a, b, t)
	return (1 - t) * a + t * b

def lerpColor(color1, color2, t)
	return [lerp(color1[0], color2[0]), lerp(color1[1], color2[1]), lerp(color1[2], color2[2])]

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
