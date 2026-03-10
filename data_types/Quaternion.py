from .Matrix3 import Matrix3

class Quaternion:
    def __init__(self, x, y, z, w):
        self.x = x
        self.y = y
        self.z = z
        self.w = w
    def toRotationMatrix(self):
        q = self.unitize()
        xx = 2 * q.x * q.x
        xy = 2 * q.x * q.y
        xz = 2 * q.x * q.z
        xw = 2 * q.x * q.w
        
        yy = 2 * q.y * q.y
        yz = 2 * q.y * q.z
        yw = 2 * q.y * q.w
        
        zz = 2 * q.z * q.z
        zw = 2 * q.z * q.w
        
        return Matrix3(1 - yy - zz, xy - zw, xz + yw, xy + zw, 1 - xx - zz, yz - xw, xz - yw, yz + xw, 1 - xx - yy)