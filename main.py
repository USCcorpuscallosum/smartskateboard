#!/usr/bin/python

from sense_hat import SenseHat, ACTION_PRESSED, DIRECTION_UP, DIRECTION_LEFT, DIRECTION_DOWN, DIRECTION_RIGHT
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

sense = SenseHat()
board = Skateboard(sense)

board.tilt_angle = math.radians(20) # Pi is at a ~20 degree incline
board.forward = Vector3(math.cos(board.tilt_angle), 0, math.sin(board.tilt_angle))

# Change mode with joystick events
mode = 0
last_mode = 0
def handle_joystick(event):
    global mode
    if event.action == ACTION_PRESSED:
        if event.direction == DIRECTION_UP or event.direction == DIRECTION_LEFT:
            mode = (mode - 1) % MODE_COUNT
        elif event.direction == DIRECTION_DOWN or event.direction == DIRECTION_RIGHT:
            mode = (mode + 1) % MODE_COUNT
sense.stick.direction_any = handle_joystick

last_board_state = Motion.stopped
all_lights = lights.Layout((0, 107))
left_lights = lights.Layout((91, 36))
right_lights = lights.Layout((92, 107), (0, 35))

# Create modes
# 0: red/yellow chase with velocity (fight on!)
# 1: red/yellow wipe
# 2: flashlight
# 3: rainbow cycle
# 4: theater chase rainbow
# 5: red/green chase with velocity
# 6: forward/backward
# 7: spinner
MODE_COUNT = 8
M0_PATTERN = [0x00ff0000, 0x00ff0000, 0x00000000, 0x00ffff00, 0x00ffff00, 0x00000000, 0x00000000,]
m1_left = left_lights.createMultiColorWipe([0x00ff0000, 0x00ffff00])
m1_right = right_lights.createMultiColorWipe([0x00ff0000, 0x00ffff00])
m3_left = left_lights.createRainbowCycle()
m3_right = right_lights.createRainbowCycle()
m4_left = left_lights.createTheaterChaseRainbow()
m4_right = right_lights.createTheaterChaseRainbow()
M5_PATTERN = [0x00ff0000, 0x00000000, 0x00000000, 0x0000ff00, 0x00000000, 0x00000000]
m7_all = all_lights.createWorm(0x00ffff00, 0x00ff0000, 15)

# Main loop
for i in infinity():
    # start = time.time()

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
    if i % 2 == 0: # update every 50ms
        if mode != last_mode:
            left_lights.clear()
            right_lights.clear()
            last_mode = mode

        if mode == 0:
            left_lights.patternOffsetDistance(M0_PATTERN, -board.distance)
            right_lights.patternOffsetDistance(M0_PATTERN, -board.distance)
        elif mode == 1:
            next(m1_left)
            next(m1_right)
        elif mode == 2:
            left_lights.color(0xffffffff)
            right_lights.color(0xffffffff)
        elif mode == 3:
            next(m3_left)
            next(m3_right)
        elif mode == 4:
            next(m4_left)
            next(m4_right)
        elif mode == 5:
            left_lights.patternOffsetDistance(M5_PATTERN, -board.distance)
            right_lights.patternOffsetDistance(M5_PATTERN, -board.distance)
        elif mode == 6:
            if board.state == Motion.forward:
                left_lights.color(0x0000ff00)
                right_lights.color(0x0000ff00)
            elif board.state == Motion.backward:
                left_lights.color(0x00ff0000)
                right_lights.color(0x00ff0000)
            else:
                left_lights.color(0x00000000)
                right_lights.color(0x00000000)
        elif mode == 7:
            next(m7_all)

    # duration = time.time() - start
    # if UPDATE_TIME > duration:
    #     time.sleep(UPDATE_TIME - duration)
