#!/usr/bin/python

# TODO
# - what if they are going in the other direction?
# - fade in to color
# - wipe forward/backward with color - like audi

# https://learn.adafruit.com/neopixels-on-raspberry-pi/overview
# https://github.com/jgarff/rpi_ws281x
# http://abyz.co.uk/rpi/pigpio/python.html
# https://wiki.qt.io/Apt-get_Qt4_on_the_Raspberry_Pi

# Axes:
# +x: toward sd card
# +y: toward gpio pins
# +z: up

import time, math
from sense_hat import SenseHat

sense = SenseHat()

# Which direction is forward
FORWARD_VEC = {'x': 1, 'y': 0, 'z': 0}

ZERO_THRESHOLD = 0.1
MAX_ACCELERATION = 1.0

# We could create individual variables for the three RGB variables that change at different rates and use inside the color functions
# That way we could have unique color combinations according to not only acceleration, but also direction
OFF_COLOR = [0, 0, 0]
FORWARD_COLOR = [0, 255, 0]
BACKWARD_COLOR = [255, 0, 0]

msleep = lambda x: time.sleep(x / 1000.0)

# Dot product of two vectors
def dot(vec1, vec2):
    return vec1['x'] * vec2['x'] + vec1['y'] * vec2['y'] + vec1['z'] * vec2['z']

# Blend between two numbers
def lerp(a, b, t):
	return (1 - t) * a + t * b

# Map x to the range 0..1 in the range min..max
def map(x, min, max):
	if x <= min:
		return min
	if x >= max:
		return max
	return (x - min) / (max - min)

# Blend between two colors
def lerpColor(color1, color2, t):
	return [
		math.floor(lerp(color1[0], color2[0], t)),
		math.floor(lerp(color1[1], color2[1], t)),
		math.floor(lerp(color1[2], color2[2], t))]

def get_forward_acceleration():
    raw = sense.get_accelerometer_raw()
    # print("{x}\t{y}\t{z}".format(**raw))

    return dot(raw, FORWARD_VEC)

while True:
    acc = get_forward_acceleration()
    if acc > ZERO_THRESHOLD:
        # sense.clear(FORWARD_COLOR)
        sense.clear(lerpColor(OFF_COLOR, FORWARD_COLOR, map(acc, ZERO_THRESHOLD, MAX_ACCELERATION)))
    elif acc < -ZERO_THRESHOLD:
        # sense.clear(BACKWARD_COLOR)
        sense.clear(lerpColor(OFF_COLOR, BACKWARD_COLOR, map(acc, ZERO_THRESHOLD, MAX_ACCELERATION)))
    else:
        sense.clear(OFF_COLOR)

    msleep(2)
