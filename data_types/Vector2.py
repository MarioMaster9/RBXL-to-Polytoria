class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def copy(self):
        return Vector2(self.x, self.y)
    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)
    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)
    def __neg__(self):
        return Vector2(-self.x, -self.y)
    def __mul__(self, other):
        othertype = type(other)
        if othertype is int or othertype is float:
            return Vector2(self.x * other, self.y * other)
        else:
            return Vector2(self.x * other.x, self.y * other.y)
    def __rmul__(self, other):
        othertype = type(other)
        if othertype is int or othertype is float:
            return Vector2(other * self.x, other * self.y)
        else:
            return Vector2(other.x * self.x, other.y * self.y)
    def __truediv__(self, rkVector):
        return Vector2(self.x / rkVector.x, self.y / rkVector.y)
    def add(self, other):
        self.x = self.x + other.x
        self.y = self.y + other.y
    @staticmethod
    def FromXML(elem):
        x = float(elem.find("X").text)
        y = float(elem.find("Y").text)
        return Vector2(x, y)
Vector2.ZERO = Vector2(0, 0)

Vector2.ONE = Vector2(1, 1)
