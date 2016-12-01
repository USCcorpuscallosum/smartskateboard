#!/usr/bin/python

import sys, threading, time
from sense_hat import SenseHat
from skateboard import *

def mark_input():
    i = 1
    while True:
        sys.stdin.readline()
        print('{:>20s}\t{:>20s}\t{}'.format('----- MARK -----', '----- MARK -----', i))
        i += 1

sense = SenseHat()
board = Skateboard(sense)

print('Press Enter to mark a time.\n')
mark_thread = threading.Thread(target = mark_input)
mark_thread.daemon = True
mark_thread.start()

print('{:>20s}\t{:>20s}'.format('Forward acceleration', 'Magnetic field'))
while True:
    board.update_forward_acceleration()
    board.update_magnet()

    print('{:20.4f}\t{:20.4f}'.format(board.forward_acceleration, board.magnet))

    time.sleep(0.005)
