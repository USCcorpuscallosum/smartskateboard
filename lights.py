import time, math, sys
from neopixel import *
from util import lerpColor, fmap

# LED strip configuration
LED_COUNT      = 120     # Number of LED pixels
LED_PIN        = 18      # (BCM 18 = board pin 12) GPIO pin connected to the pixels (must support PWM!)
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0
LED_STRIP      = ws.WS2811_STRIP_GRB

LIGHT_DISTANCE = 0.015  # Light separation distance (m)

strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
strip.begin()

def wheel(pos):
    """
    Generate rainbow colors across 0-255 positions.
    From https://github.com/jgarff/rpi_ws281x/blob/master/python/examples/strandtest.py
    """
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)

def infinity():
    return range(sys.maxint)

class LightRange:
    def __init__(self, first, last):
        """Use a range of pixels, from first to last (inclusive)."""
        self.start = first
        self.step = 1 if last >= first else -1 # for iteration
        self.end = last + self.step # 1 past going either direction
        self.length = math.abs(self.end - self.start)

    def clear(self):
        self.color(0x000000)

    def color(self, color):
        """A single color."""
        for i in range(self.start, self.end, self.step):
            strip.setPixelColor(i, color)
        strip.show()

    def patternOffsetDistance(self, pattern, distance):
        """Show a pattern, offset along the strip using a physical distance."""
        offset = int(distance / LIGHT_DISTANCE)
        for i in range(0, self.length):
            strip.setPixelColor(self.start + self.step * i, pattern[(offset + i) % len(pattern)])
        strip.show()

    def createColorWipe(self, color):
        """Generator to wipe color across display a pixel at a time. Based on rpi_ws281x strandtest."""
        for i in range(self.start, self.end, self.step):
            strip.setPixelColor(i, color)
            strip.show()
            yield True
        yield False

    def createTheaterChase(self, color):
        """Generator with movie theater light style chaser animation. Based on rpi_ws281x strandtest."""
        while True:
            for q in range(3):
                for i in range(self.start, self.end, 3 * self.step):
                    strip.setPixelColor(i + q, color)
                strip.show()
                yield True
                for i in range(self.start, self.end, 3 * self.step):
                    strip.setPixelColor(i + q, 0)

    def createRainbow(self):
        """Generator to draw rainbow that fades across all pixels at once. Based on rpi_ws281x strandtest."""
        for j in infinity():
            for i in range(self.start, self.end, self.step):
                strip.setPixelColor(i, wheel((i + j) & 255))
            strip.show()
            yield True

    def createRainbowCycle(self):
        """Generator to draw rainbow that uniformly distributes itself across all pixels. Based on rpi_ws281x strandtest."""
        for j in infinity():
            for i in range(self.start, self.end, self.step):
                strip.setPixelColor(i, wheel(((i * 256 / self.length) + j) & 255))
            strip.show()
            yield True

    def createTheaterChaseRainbow(self):
        """Generator with rainbow movie theater light style chaser animation. Based on rpi_ws281x strandtest."""
        for j in infinity():
            for q in range(3):
                for i in range(self.start, self.end, 3 * self.step):
                    strip.setPixelColor(i + q, wheel((i + j) % 255))
                strip.show()
                yield True
                for i in range(self.start, self.end, 3 * self.step):
                    strip.setPixelColor(i + q, 0)


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
