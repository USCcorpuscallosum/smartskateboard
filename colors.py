#!/usr/bin/python

# TODO
# - what if they are going in the other direction?
# - fade in to color
# - wipe forward/backward with color - like audi
# - architect for different configurations - bike, skateboard, golf cart, input, etc. for tech coolness

# Axes:
# +x: toward sd card
# +y: toward gpio pins
# +z: up
# pitch: toward sd
# roll: toward hdmi

import math
from euclid import *
from sense_hat import SenseHat
from util import msleep, dot, fmap, lerpColor

sense = SenseHat()

# Which direction is forward
FORWARD_VEC = Vector3(1, 0, 0)

ZERO_THRESHOLD = 0.05
MAX_ACCELERATION = 1.0

# We could create individual variables for the three RGB variables that change at different rates and use inside the color functions
# That way we could have unique color combinations according to not only acceleration, but also direction
OFF_COLOR = [0, 0, 0]
FORWARD_COLOR = [0, 255, 0]
BACKWARD_COLOR = [255, 0, 0]

# Compensate the accelerometer readings from gravity.
# http://www.varesano.net/blog/fabio/simple-gravity-compensation-9-dom-imus
# @param q the quaternion representing the orientation
# @param acc acceleration in g
# @return a vector representing dynamic acceleration in g
def gravity_compensate(q, acc):
    g = Vector3()

    # get expected direction of gravity
    g.x = 2 * (q.y * q.w - q.x * q.z)
    g.y = 2 * (q.x * q.y + q.z * q.w)
    g.z = q.x * q.x - q.y * q.y - q.z * q.z + q.w * q.w

    # compensate accelerometer readings with the expected direction of gravity
    return Vector3(acc.x - g.x, acc.y - g.y, acc.z - g.z)

def get_forward_acceleration():
    raw_acc = sense.get_accelerometer_raw()
    # print("{x}\t{y}\t{z}".format(**raw_acc))
    acceleration = Vector3(raw_acc['x'], raw_acc['y'], raw_acc['z'])

    angles = sense.get_orientation_radians()
    rotation = Quaternion.new_rotate_euler(
        -angles['pitch'], # around y
        angles['roll'],   # around x
        angles['yaw'])    # around z

    # gravity = Vector3(0, 0, 1)
    # gravity = rotation.get_matrix().inverse() * gravity
    # new_acceleration = acceleration - gravity

    new_acceleration = gravity_compensate(rotation, acceleration)
    # print('{}\t{}\t{}\t{}\t{}\t{}'.format(acceleration.x, acceleration.y, acceleration.z, new_acceleration.x, new_acceleration.y, new_acceleration.z))

    return new_acceleration.dot(FORWARD_VEC)

# def get_forward_acceleration_old():
#   raw = sense.get_accelerometer_raw()
#   temp = raw.copy()
#
#   gyro = sense.get_gyroscope()
#   # print("{pitch}\t{roll}\t{yaw}".format(**gyro))
#
#   raw['x'] += math.sin(math.radians(gyro['pitch'])) * 1.0
#   raw['y'] -= math.sin(math.radians(gyro['roll'])) * 1.0
#   # print("{x}\t{y}\t{z}".format(**raw))
#   print('{}\t{}\t{}\t{}\t{}\t{}'.format(temp['x'], temp['y'], temp['z'], raw['x'], raw['y'], raw['z']))
#   return raw;

while True:
    acc = get_forward_acceleration()
    if acc > ZERO_THRESHOLD:
        # sense.clear(FORWARD_COLOR)
        sense.clear(lerpColor(OFF_COLOR, FORWARD_COLOR, fmap(acc, ZERO_THRESHOLD, MAX_ACCELERATION)))
    elif acc < -ZERO_THRESHOLD:
        # sense.clear(BACKWARD_COLOR)
        sense.clear(lerpColor(OFF_COLOR, BACKWARD_COLOR, fmap(-acc, ZERO_THRESHOLD, MAX_ACCELERATION)))
    else:
        sense.clear(OFF_COLOR)

    msleep(2)
