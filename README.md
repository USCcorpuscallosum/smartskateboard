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
```
