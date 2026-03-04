from .Vector2 import Vector2

class UDim2:
    def __init__(self, scale, offset):
        self.scale = scale
        self.offset = offset
    @staticmethod
    def FromXML(elem):
        xs = float(elem.find("XS").text)
        xo = float(elem.find("XO").text)
        ys = float(elem.find("YS").text)
        yo = float(elem.find("YO").text)
        return UDim2(Vector2(xs, ys), Vector2(xo, yo))