import math
from .Vector2 import Vector2
import data_types.Enum as Enum

class Vector3:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    def copy(self):
        return Vector3(self.x, self.y, self.z)
    def __iter__(self):
        return iter((self.x, self.y, self.z))
    def __add__(self, other):
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)
    def __sub__(self, other):
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)
    def __neg__(self):
        return Vector3(-self.x, -self.y, -self.z)
    def __mul__(self, other):
        othertype = type(other)
        if othertype is int or othertype is float:
            return Vector3(self.x * other, self.y * other, self.z * other)
        else:
            return Vector3(self.x * other.x, self.y * other.y, self.z * other.z)
    def __rmul__(self, other):
        othertype = type(other)
        if othertype is int or othertype is float:
            return Vector3(other * self.x, other * self.y, other * self.z)
        else:
            return Vector3(other.x * self.x, other.y * self.y, other.z * self.z)
    def add(self, other):
        self.x = self.x + other.x
        self.y = self.y + other.y
        self.z = self.z + other.z
    def dot(self, rkVector):
        return self.x*rkVector.x + self.y*rkVector.y + self.z*rkVector.z
    def magnitude(self):
        return math.sqrt(self.x*self.x + self.y*self.y + self.z*self.z)
    def cross(self, rkVector):
        return Vector3(self.y*rkVector.z - self.z*rkVector.y, self.z*rkVector.x - self.x*rkVector.z, self.x*rkVector.y - self.y*rkVector.x)
    def unitize (self, fTolerance=1e-06):
        fMagnitude = self.magnitude()

        if fMagnitude > fTolerance:
            fInvMagnitude = 1 / fMagnitude
            self.x *= fInvMagnitude
            self.y *= fInvMagnitude
            self.z *= fInvMagnitude
        else:
            fMagnitude = 0

        return fMagnitude
    def squaredMagnitude(self):
        return self.x*self.x + self.y*self.y + self.z*self.z
    def direction(self):
        lenSquared = self.squaredMagnitude()
        invSqrt = 1 / math.sqrt(lenSquared)
        return Vector3(self.x * invSqrt, self.y * invSqrt, self.z * invSqrt)
    def clamp(self, _min, _max):
        self.x = max(min(self.x, _max.x), _min.x)
        self.y = max(min(self.y, _max.y), _min.y)
        self.z = max(min(self.z, _max.z), _min.z)
    def xx(self):
        return Vector2(self.x, self.x)
    def yx(self):
        return Vector2(self.y, self.x)
    def zx(self):
        return Vector2(self.z, self.x)
    def xy(self):
        return Vector2(self.x, self.y)
    def yy(self):
        return Vector2(self.y, self.y)
    def zy(self):
        return Vector2(self.z, self.y)
    def xz(self):
        return Vector2(self.x, self.z)
    def yz(self):
        return Vector2(self.y, self.z)
    def zz(self):
        return Vector2(self.z, self.z)
    def xxx(self):
        return Vector3(self.x, self.x, self.x)
    def yxx(self):
        return Vector3(self.y, self.x, self.x)
    def zxx(self):
        return Vector3(self.z, self.x, self.x)
    def xyx(self):
        return Vector3(self.x, self.y, self.x)
    def yyx(self):
        return Vector3(self.y, self.y, self.x)
    def zyx(self):
        return Vector3(self.z, self.y, self.x)
    def xzx(self):
        return Vector3(self.x, self.z, self.x)
    def yzx(self):
        return Vector3(self.y, self.z, self.x)
    def zzx(self):
        return Vector3(self.z, self.z, self.x)
    def xxy(self):
        return Vector3(self.x, self.x, self.y)
    def yxy(self):
        return Vector3(self.y, self.x, self.y)
    def zxy(self):
        return Vector3(self.z, self.x, self.y)
    def xyy(self):
        return Vector3(self.x, self.y, self.y)
    def yyy(self):
        return Vector3(self.y, self.y, self.y)
    def zyy(self):
        return Vector3(self.z, self.y, self.y)
    def xzy(self):
        return Vector3(self.x, self.z, self.y)
    def yzy(self):
        return Vector3(self.y, self.z, self.y)
    def zzy(self):
        return Vector3(self.z, self.z, self.y)
    def xxz(self):
        return Vector3(self.x, self.x, self.z)
    def yxz(self):
        return Vector3(self.y, self.x, self.z)
    def zxz(self):
        return Vector3(self.z, self.x, self.z)
    def xyz(self):
        return Vector3(self.x, self.y, self.z)
    def yyz(self):
        return Vector3(self.y, self.y, self.z)
    def zyz(self):
        return Vector3(self.z, self.y, self.z)
    def xzz(self):
        return Vector3(self.x, self.z, self.z)
    def yzz(self):
        return Vector3(self.y, self.z, self.z)
    def zzz(self):
        return Vector3(self.z, self.z, self.z)
    @staticmethod
    def FromNormalId(norm):
        match norm:
            case Enum.NormalId.Right:
                return Vector3(1, 0, 0)
            case Enum.NormalId.Top:
                return Vector3(0, 1, 0)
            case Enum.NormalId.Back:
                return Vector3(0, 0, 1)
            case Enum.NormalId.Left:
                return Vector3(-1, 0, 0)
            case Enum.NormalId.Bottom:
                return Vector3(0, -1, 0)
            case Enum.NormalId.Front:
                return Vector3(0, 0, -1)
    @staticmethod
    def FromXML(elem):
        x = float(elem.find("X").text)
        y = float(elem.find("Y").text)
        z = float(elem.find("Z").text)
        return Vector3(x, y, z)

Vector3.unitX = Vector3(1, 0, 0)
Vector3.unitY = Vector3(0, 1, 0)
Vector3.unitZ = Vector3(0, 0, 1)
Vector3.ZERO = Vector3(0, 0, 0)
Vector3.ONE = Vector3(1, 1, 1)