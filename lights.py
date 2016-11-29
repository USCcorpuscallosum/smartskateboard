from neopixel import *
from util import lerpColor, fmap

# LED strip configuration
LED_COUNT      = 60      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0
LED_STRIP      = ws.SK6812_STRIP_RGBW

strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
strip.begin()

# https://github.com/jgarff/rpi_ws281x/blob/master/python/examples/SK6812_strandtest.py

class Gradient:
    def __init__(self, points, colors):
        self.points = points
        self.count = len(points)
        self.colors = colors

    def get(self, t):
        # Find the point which is just greater than t
        i = 0
        while i < self.count and self.points[i] < t:
            i += 1

        if i == 0:
            return self.colors[0]
        if i == self.count:
            return self.colors[self.count - 1]
        return lerpColor(self.colors[i - 1], self.colors[i], fmap(t, self.points[i - 1], self.points[i]))
