#!/usr/bin/python

from sense_hat import SenseHat
from skateboard import *
# from lights import *
from util import msleep, fmap, SenseHatColor

# TODO
# - architect for different configurations - bike, skateboard, golf cart, input, etc. for tech coolness
# - provide acceleration, velocity, compass input to color fn
# - what if they are going in the other direction?
# - wipe forward/backward with color - like audi

# We could create individual variables for the three RGB variables that change at different rates and use inside the color functions
# That way we could have unique color combinations according to not only acceleration, but also direction
OFF_COLOR      = 0x000000
FORWARD_COLOR  = 0x00ff00
BACKWARD_COLOR = 0xff0000

sense = SenseHat()
board = Skateboard(sense)

while True:
    board.update_forward_acceleration()
    board.update_magnet()
    board.update()

    if board.state == Motion.forward:
        sense.clear(SenseHatColor(FORWARD_COLOR))
    elif board.state == Motion.backward:
        sense.clear(SenseHatColor(BACKWARD_COLOR))
    else:
        sense.clear(SenseHatColor(OFF_COLOR))

    msleep(2)
