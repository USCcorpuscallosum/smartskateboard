import math, time
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

        # Configuration
        self.forward = Vector3(1, 0, 0)             # Forward direction normalized vector
        self.zero_acceleration = 0.05               # Threshold for no acceleration
        self.max_acceleration = 1.0                 # Max possible acceleration
        self.wheel_radius = 0.03                    # Wheel radius in m # TODO: measure
        self.wheel_magnet_near_threshold = 303154   # Close nagnetic threshold in uT (micro teslas) # TODO: measure, 4cm
        self.wheel_magnet_far_threshold = 76797     # Far magnetic threshold # TODO: measure, 2cm
        self.speed_smoothing = 0

        # Sensor data
        self.forward_acceleration = 0
        self.compass = 0
        self.magnet = 0

        # Computed values
        self.state = Motion.stopped
        self.speed = 0;

        # Internal
        self._prev_forward_acceleration = 0
        self._magnet_near = False
        self._last_magnet_near_time = 0

    def update(self):
        # Change motion state when we pass a threshold
        if self.state == Motion.stopped:
            if self._prev_forward_acceleration < self.zero_acceleration and self.forward_acceleration >= self.zero_acceleration:
                self.state = Motion.forward
                # print('forward <- stop')
            elif self._prev_forward_acceleration > -self.zero_acceleration and self.forward_acceleration <= -self.zero_acceleration:
                self.state = Motion.backward
                # print('backward <- stop')
        elif self.state == Motion.forward and self.forward_acceleration <= -self.zero_acceleration:
            self.state = Motion.stopped
            # print('stop <- forward')
        elif self.state == Motion.backward and self.forward_acceleration >= self.zero_acceleration:
            self.state = Motion.stopped
            # print('stop <- backward')

        # Calculate speed from magnetic field strength
        if (self._magnet_near and self.magnet < self.wheel_magnet_far_threshold) or (not self._magnet_near and self.magnet > self.wheel_magnet_near_threshold):
            # Update near state if we passed a threshold
            self._magnet_near = not self._magnet_near

            if self._magnet_near:
                # Calculate the speed using the time difference between this time and the last time
                now = time.time()
                if self._last_magnet_near_time > 0:
                    dt = now - self._last_magnet_near_time

                    # speed = distance / time
                    # distance = circumference of wheel = 2*pi*r
                    new_speed = 2. * math.pi * self.wheel_radius / dt

                    # Smooth speed a little
                    self.speed = self.speed * self.speed_smoothing + new_speed * (1. - self.speed_smoothing)
                self._last_magnet_near_time = now

    def update_forward_acceleration(self):
        self._prev_forward_acceleration = self.forward_acceleration

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

    def update_compass(self):
        orientation = self.sense.get_orientation_degrees()
        self.compass = orientation['yaw']

    def update_magnet(self):
        # Magnetometer raw data in uT (micro teslas)
        raw = self.sense.get_compass_raw()

        magnitudeSq = raw['x'] * raw['x'] + raw['y'] * raw['y'] + raw['z'] * raw['z']
        self.magnet = magnitudeSq

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
