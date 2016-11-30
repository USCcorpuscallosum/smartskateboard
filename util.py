import time

msleep = lambda x: time.sleep(x / 1000.0)

# Dot product of two vectors
def dot(vec1, vec2):
    return vec1['x'] * vec2['x'] + vec1['y'] * vec2['y'] + vec1['z'] * vec2['z']

# Blend between a and b by t
def lerp(a, b, t):
    return (1 - t) * a + t * b

# Map x to the range 0..1 from the range min..max
def fmap(x, min, max):
    if x <= min:
        return min
    if x >= max:
        return max
    return (x - min) / (max - min)

# Blend between two colors by t
def lerpColor(color1, color2, t):
    # See neopixel.Color
    # https://github.com/jgarff/rpi_ws281x/blob/master/python/neopixel.py#L8

    return \
        (int(lerp((color1 & 0xff000000) >> 24, (color2 & 0xff000000) >> 24, t)) << 24) | \
        (int(lerp((color1 & 0x00ff0000) >> 16, (color2 & 0x00ff0000) >> 16, t)) << 16) | \
        (int(lerp((color1 & 0x0000ff00) >>  8, (color2 & 0x0000ff00) >>  8, t)) <<  8) | \
        (int(lerp((color1 & 0x000000ff)      , (color2 & 0x000000ff)      , t))      )

# Blend between two colors by t
def lerpSenseHatColor(color1, color2, t):
    return [
        int(lerp(color1[0], color2[0], t)),
        int(lerp(color1[1], color2[1], t)),
        int(lerp(color1[2], color2[2], t))]

def SenseHatColor(color):
    return [
        (color & 0xff0000) >> 16,
        (color & 0x00ff00) >>  8,
        (color & 0x0000ff)]
