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
    return [
        int(lerp(color1[0], color2[0], t)),
        int(lerp(color1[1], color2[1], t)),
        int(lerp(color1[2], color2[2], t))]
