import struct

extract_argb = struct.Struct('>I').pack

class Color3:
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b
    def __eq__(self, rkVector):
        return self.r == rkVector.r and self.g == rkVector.g and self.b == rkVector.b
    def __ne__(self, rkVector):
        return self.r != rkVector.r or self.g != rkVector.g or self.b != rkVector.b
    def __add__(self, rkVector):
        return Color3(self.r + rkVector.r, self.g + rkVector.g, self.b + rkVector.b)
    def __sub__(self, rkVector):
        return Color3(self.r - rkVector.r, self.g - rkVector.g, self.b - rkVector.b)
    def __mul__(self, v):
        argtype = type(v)
        if argtype is float:
            fScalar = v
            return Color3(fScalar*self.r, fScalar*self.g, fScalar*self.b)
        elif argtype is Color3:
            rkVector = v
            return Color3(self.r * rkVector.r, self.g  * rkVector.g, self.b * rkVector.b)
        raise NotImplementedError
    def __neg__(self):
        return Color3(-self.r, -self.g, -self.b)
    @staticmethod
    def FromXML(elem):
        if elem.find("R") is None:
            color = int(elem.text)
            a, r, g, b = extract_argb(color & 0xFFFFFFFF)
            return Color3(r/255, g/255, b/255)
        r = float(elem.find("R").text)
        g = float(elem.find("G").text)
        b = float(elem.find("B").text)
        return Color3(r, g, b)
Color3.BLACK = Color3(0, 0, 0)
Color3.WHITE = Color3(1, 1, 1)