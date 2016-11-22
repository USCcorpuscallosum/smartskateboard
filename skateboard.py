import math
from euclid import *

# Axes:
# +x: toward sd card
# +y: toward gpio pins
# +z: up
# pitch: toward sd
# roll: toward hdmi

class Motion:
    backward = -1
    stopped = 0
    forward = 1

class Skateboard:
    def __init__(self, sense):
        self.sense = sense;
        # Forward direction normalized vector
        self.forward = Vector3(1, 0, 0)
        # Threshold for no acceleration
        self.zero_acceleration = 0.05
        # Max possible acceleration
        self.max_acceleration = 1.0
        # Wheel radius in m
        self.wheel_radius = 0.03 # TODO: measure
        # Hall effect threshold in uT (micro teslas)
        self.wheel_magnet_threshold = 0 # TODO: measure

        # Motion state
        self.state = Motion.stopped
        self.prev_forward_acceleration = 0
        self.forward_acceleration = 0

    def update(self):
        self.update_forward_acceleration()

        # Change motion state when we pass a threshold
        if self.state == Motion.stopped:
            if self.prev_forward_acceleration < self.zero_acceleration and self.forward_acceleration >= self.zero_acceleration:
                self.state = Motion.forward
                # print('forward <- stop')
            elif self.prev_forward_acceleration > -self.zero_acceleration and self.forward_acceleration <= -self.zero_acceleration:
                self.state = Motion.backward
                # print('backward <- stop')
        elif self.state == Motion.forward and self.forward_acceleration <= -self.zero_acceleration:
            self.state = Motion.stopped
            # print('stop <- forward')
        elif self.state == Motion.backward and self.forward_acceleration >= self.zero_acceleration:
            self.state = Motion.stopped
            # print('stop <- backward')

    def update_forward_acceleration(self):
        self.prev_forward_acceleration = self.forward_acceleration

        raw_acc = self.sense.get_accelerometer_raw()
        # print("{x}\t{y}\t{z}".format(**raw_acc))
        acceleration = Vector3(raw_acc['x'], raw_acc['y'], raw_acc['z'])

        angles = self.sense.get_orientation_radians()
        rotation = Quaternion.new_rotate_euler(
            -angles['pitch'], # around y
            angles['roll'],   # around x
            angles['yaw'])    # around z

        # gravity = Vector3(0, 0, 1)
        # gravity = rotation.get_matrix().inverse() * gravity
        # new_acceleration = acceleration - gravity

        new_acceleration = self.__gravity_compensate(rotation, acceleration)
        # print('{}\t{}\t{}\t{}\t{}\t{}'.format(acceleration.x, acceleration.y, acceleration.z, new_acceleration.x, new_acceleration.y, new_acceleration.z))
        self.forward_acceleration = new_acceleration.dot(self.forward)

    # def get_forward_acceleration_old(self):
    #     raw = self.sense.get_accelerometer_raw()
    #     temp = raw.copy()
    #
    #     gyro = self.sense.get_gyroscope()
    #     # print("{pitch}\t{roll}\t{yaw}".format(**gyro))
    #
    #     raw['x'] += math.sin(math.radians(gyro['pitch'])) * 1.0
    #     raw['y'] -= math.sin(math.radians(gyro['roll'])) * 1.0
    #     # print("{x}\t{y}\t{z}".format(**raw))
    #     print('{}\t{}\t{}\t{}\t{}\t{}'.format(temp['x'], temp['y'], temp['z'], raw['x'], raw['y'], raw['z']))
    #     return raw;

    def get_compass(self):
        orientation = self.sense.get_orientation_degrees()
        return orientation['yaw']

    def get_hall(self):
        # Magnetometer raw data in uT (micro teslas)
        raw = self.sense.get_compass_raw()
        print("{x}\t{y}\t{z}".format(**raw))

        magnitude = Vector3(raw['x'], raw['y'], raw['z']).magnitude()
        print(magnitude)
        return magnitude

    # Compensate the accelerometer readings from gravity.
    # http://www.varesano.net/blog/fabio/simple-gravity-compensation-9-dom-imus
    # @param q the quaternion representing the orientation
    # @param acc acceleration in g
    # @return a vector representing dynamic acceleration in g
    def __gravity_compensate(self, q, acc):
        g = Vector3()

        # get expected direction of gravity
        g.x = 2 * (q.y * q.w - q.x * q.z)
        g.y = 2 * (q.x * q.y + q.z * q.w)
        g.z = q.x * q.x - q.y * q.y - q.z * q.z + q.w * q.w

        # compensate accelerometer readings with the expected direction of gravity
        return Vector3(acc.x - g.x, acc.y - g.y, acc.z - g.z)