from .Color3 import Color3

class Color4:
    def __init__(self, r, g, b, a):
        self.r = r
        self.g = g
        self.b = b
        self.a = a
    def setColor3(self, c):
        self.r = c.r
        self.g = c.g
        self.b = c.b
    def __rmul__(self, v):
        argtype = type(v)
        if argtype is Color3:
            c3 = v
            c4 = self
            return Color4(c3.r * c4.r, c3.g * c4.g, c3.b * c4.b, c4.a)
        elif argtype is float:
            fScalar = v
            return Color4(fScalar * self.r, fScalar * self.g, fScalar * self.b, fScalar * self.a)
        raise NotImplementedError
    def __mul__(self, v):
        argtype = type(v)
        if argtype is Color3:
            c3 = v
            c4 = self
            return Color4(c4.r * c3.r, c4.g * c3.g, c4.b * c3.b, c4.a)
        elif argtype is float:
            fScalar = v
            return Color4(self.r * fScalar, self.g * fScalar, self.b * fScalar, self.a * fScalar)
        raise NotImplementedError
    @staticmethod
    def FromColor3(color, alpha=1):
        return Color4(color.r, color.g, color.b, alpha)
Color4.WHITE = Color4(1, 1, 1, 1)