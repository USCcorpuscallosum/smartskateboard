# Smart Skateboard
Smart skateboards and bikes. Fall 2016.

## Raspberry Pi Setup

```sh
passwd
# default: raspberry
# new: skateboard

sudo apt-get update
sudo apt-get install sense-hat
sudo apt-get install build-essential python-dev git scons swig # for rpi_ws281x
sudo reboot

git clone https://github.com/jgarff/rpi_ws281x.git
cd rpi_ws281x
scons
cd python
sudo python setup.py install

git clone https://github.com/usccorpuscallosum/smartskateboard.git /home/pi/skateboard

# Start program on boot
sudo echo "python /home/pi/skateboard/main.py" >> /etc/rc.local

# Run
python /home/pi/skateboard/main.py
```

#### Copy code to Pi (from laptop)

```sh
cd smartskateboard
scp *.py pi@raspberrypi.local:/home/pi/skateboard
```

#### Kill running process

```sh
pkill -fe skateboard/main.py
```

## Resources
- https://learn.adafruit.com/neopixels-on-raspberry-pi/overview
- https://github.com/jgarff/rpi_ws281x
- http://abyz.co.uk/rpi/pigpio/python.html
- https://wiki.qt.io/Apt-get_Qt4_on_the_Raspberry_Pi
- https://learn.adafruit.com/flora-brakelight-backpack/the-code
