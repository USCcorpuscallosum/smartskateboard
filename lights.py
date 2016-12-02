import time, sys
from neopixel import *
from util import lerpColor, fmap, infinity

# LED strip configuration
LED_COUNT      = 108     # Number of LED pixels
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

class Range:
    def __init__(self, first, last):
        """A range of numbers, from first to last (inclusive), in positive or negative direction."""
        self.start = first
        self.step = 1 if last >= first else -1 # for iteration
        self.end = last + self.step # 1 past going either direction
        self.length = abs(self.end - self.start)

    def range(self):
        return range(self.start, self.end, self.step)

class Layout:
    def __init__(self, *ranges):
        """Use one or more ranges of pixels, each with a first and last index (inclusive)."""
        self.layout = []
        self.length = 0
        for r in ranges:
            sub_range = Range(r[0], r[1])
            self.layout.append(sub_range)
            self.length += sub_range.length

    def pixel_layout(self):
        """Get a generator for each pixel index in this layout."""
        for r in self.layout:
            for i in r.range():
                yield i

    def get_pixel(self, i):
        """Get the ith pixel in this layout."""
        for r in self.layout:
            if i < r.length:
                return r.range()[i]
            i -= r.length
        return self.layout[-1].range()[-1] # last pixel in layout

    def clear(self):
        """Set to black."""
        self.color(0x000000)

    def color(self, color):
        """Show a single color."""
        for pixel in self.pixel_layout():
            strip.setPixelColor(pixel, color)
        strip.show()

    def patternOffsetDistance(self, pattern, distance):
        """Show a pattern, offset along the strip using a physical distance."""
        offset = int(distance / LIGHT_DISTANCE)
        pixels = self.pixel_layout()
        for pixel in range(self.length):
            strip.setPixelColor(next(pixels), pattern[(offset + pixel) % len(pattern)])
        strip.show()

    def createColorWipe(self, color):
        """Generator to wipe color across display a pixel at a time. Based on rpi_ws281x strandtest."""
        for pixel in self.pixel_layout():
            strip.setPixelColor(pixel, color)
            strip.show()
            yield True
        yield False

    def createMultiColorWipe(self, colors):
        """Generator to wipe several color across display a pixel at a time."""
        for i in infinity():
            for pixel in self.pixel_layout():
                strip.setPixelColor(pixel, colors[i % len(colors)])
                strip.show()
                yield True

    def createTheaterChase(self, color):
        """Generator with movie theater light style chaser animation. Based on rpi_ws281x strandtest."""
        while True:
            for q in range(3):
                for i in range(0, self.length, 3):
                    strip.setPixelColor(self.get_pixel(i + q), color)
                strip.show()
                yield True
                for i in range(0, self.length, 3):
                    strip.setPixelColor(self.get_pixel(i + q), 0x000000)

    def createWorm(self, background, foreground, length):
        """Generator with worm which crawls along pixels."""
        self.color(background)
        for i in range(0, length):
            strip.setPixelColor(self.get_pixel(i), foreground)
        for j in infinity():
            for i in range(0, self.length):
                strip.setPixelColor(self.get_pixel((i + length) % self.length), foreground)
                strip.setPixelColor(self.get_pixel(i), background)
                strip.show()
                yield True

    def createRainbow(self):
        """Generator to draw rainbow that fades across all pixels at once. Based on rpi_ws281x strandtest."""
        for j in infinity():
            pixels = self.pixel_layout()
            for i in range(self.length):
                strip.setPixelColor(next(pixels), wheel((i + j) & 255))
            strip.show()
            yield True

    def createRainbowCycle(self):
        """Generator to draw rainbow that uniformly distributes itself across all pixels. Based on rpi_ws281x strandtest."""
        SPEED = 5
        for j in infinity():
            pixels = self.pixel_layout()
            for i in range(self.length):
                strip.setPixelColor(next(pixels), wheel(((i * 256 / self.length) + j * SPEED) & 255))
            strip.show()
            yield True

    def createTheaterChaseRainbow(self):
        """Generator with rainbow movie theater light style chaser animation. Based on rpi_ws281x strandtest."""
        for j in infinity():
            for q in range(3):
                for i in range(0, self.length, 3):
                    strip.setPixelColor(self.get_pixel(i + q), wheel((i + j) % 255))
                strip.show()
                yield True
                for i in range(0, self.length, 3):
                    strip.setPixelColor(self.get_pixel(i + q), 0x000000)


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
