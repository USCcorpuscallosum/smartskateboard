#!/usr/bin/python

from sense_hat import SenseHat
from skateboard import *
import lights
from util import SenseHatColor, infinity

# TODO
# - what if they are going in the other direction?
# - wipe forward/backward with color - like audi

UPDATE_TIME = 0.005 # 5ms

# We could create individual variables for the three RGB variables that change at different rates and use inside the color functions
# That way we could have unique color combinations according to not only acceleration, but also direction
OFF_COLOR      = SenseHatColor(0x000000)
FORWARD_COLOR  = SenseHatColor(0x00ff00)
BACKWARD_COLOR = SenseHatColor(0xff0000)
PATTERN = [0x00ff0000, 0x00000000, 0x00000000, 0x0000ff00, 0x00000000, 0x00000000]

sense = SenseHat()
board = Skateboard(sense)

last_board_state = Motion.stopped
left_lights = lights.LightRange(0, 59)
right_lights = lights.LightRange(119, 60)

left_chase = left_lights.createTheaterChase(0x0000ff)

for i in infinity():
    board.update_forward_acceleration()
    board.update_magnet()
    board.update()

    # Show forward/backward color on SenseHAT
    if board.state != last_board_state:
        if board.state == Motion.forward:
            sense.clear(FORWARD_COLOR)
        elif board.state == Motion.backward:
            sense.clear(BACKWARD_COLOR)
        else:
            sense.clear(OFF_COLOR)
        last_board_state = board.state

    # Show lights
    if i % 10 == 0: # update every 50ms
        next(left_chase)
    right_lights.patternOffsetDistance(PATTERN, board.distance)

    time.sleep(UPDATE_TIME)
