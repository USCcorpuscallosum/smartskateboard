# pretty-lights
Coding for smart skateboards and bikes.

## Raspberry Pi Setup

```sh
passwd
# default: raspberry
# new: skateboard

sudo apt-get update
sudo apt-get install sense-hat
sudo apt-get install build-essential python-dev git scons swig # rpi_ws281x
sudo reboot

git clone https://github.com/jgarff/rpi_ws281x.git
cd rpi_ws281x
scons
cd python
sudo python setup.py install

git clone https://github.com/USCcorpuscallosum/smartskateboard.git /home/pi/skateboard
```

#### Start program on boot

```sh
sudo nano /etc/rc.local
```

Append: `python /home/pi/skateboard/colors.py`

#### Copy code to Pi (from laptop)

```sh
scp *.py pi@raspberrypi.local:/home/pi/skateboard
```

Kill running python

```sh
ps aux | grep skateboard/colors.py
sudo kill [pid]
```

## Resources
- https://learn.adafruit.com/neopixels-on-raspberry-pi/overview
- https://github.com/jgarff/rpi_ws281x
- http://abyz.co.uk/rpi/pigpio/python.html
- https://wiki.qt.io/Apt-get_Qt4_on_the_Raspberry_Pi
- https://learn.adafruit.com/flora-brakelight-backpack/the-code
