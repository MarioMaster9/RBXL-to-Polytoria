import math

# math.radians and math.degrees aren't expandable, so use multiplication 
# so that the __mul__ dunder method can be implemented in the class
degToRad = math.pi / 180
radToDeg = 180 / math.pi

def radians(v):
    return v * degToRad
def degrees(v):
    return v * radToDeg