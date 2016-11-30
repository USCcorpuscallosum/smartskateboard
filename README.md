# Smart Skateboard
Smart skateboards and bikes. Fall 2016.

## Raspberry Pi Setup

#### Set password
```sh
passwd
# default: raspberry
# new: skateboard
```

#### Install things
```sh
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
```

#### Start program on boot
```sh
sudo echo "python /home/pi/skateboard/main.py" >> /etc/rc.local
```

#### Disable audio drivers to get LEDs working
(See https://github.com/jgarff/rpi_ws281x/issues/103)

1. Add the following to /boot/config.txt:
  ```
  hdmi_force_hotplug=1
  hdmi_force_edid_audio=1
  ```
  and also prepend a `#` to the `dtparam=audio=on` line

1. Blacklist audio driver
  ```sh
  sudo echo 'blacklist snd_bcm2835' > nano /etc/modprobe.d/snd-blacklist.conf
  ```

#### Run it for the first time
```sh
sudo python /home/pi/skateboard/main.py
```

## Other commands

#### Copy code to Pi over SSH (from laptop)
```sh
cd smartskateboard
scp *.py pi@raspberrypi.local:/home/pi/skateboard
```

#### Kill running process
```sh
sudo pkill -fe skateboard/main.py
```

## Resources
- https://pythonhosted.org/sense-hat/api/
- https://github.com/jgarff/rpi_ws281x
- https://learn.adafruit.com/neopixels-on-raspberry-pi/overview
- http://abyz.co.uk/rpi/pigpio/python.html
- https://wiki.qt.io/Apt-get_Qt4_on_the_Raspberry_Pi
- https://learn.adafruit.com/flora-brakelight-backpack/the-code
- https://www.raspberrypi.org/documentation/hardware/sense-hat/images/Sense-HAT-V1_0.pdf
- https://www.raspberrypi.org/forums/viewtopic.php?t=122972&p=827474
- http://pinout.xyz/pinout/pin12_gpio18
