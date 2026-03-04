from .Vector3 import Vector3
from .Matrix3 import Matrix3

class CoordinateFrame:
    def __init__(self, rotation, translation):
        self.rotation = rotation
        self.translation = translation
    def __mul__(self, other):
        return CoordinateFrame(self.rotation * other.rotation, self.pointToWorldSpace(other.translation))
    def pointToWorldSpace(self, v):
        x = self.rotation.elt[0][0] * v.x + self.rotation.elt[0][1] * v.y + self.rotation.elt[0][2] * v.z + self.translation.x
        y = self.rotation.elt[1][0] * v.x + self.rotation.elt[1][1] * v.y + self.rotation.elt[1][2] * v.z + self.translation.y
        z = self.rotation.elt[2][0] * v.x + self.rotation.elt[2][1] * v.y + self.rotation.elt[2][2] * v.z + self.translation.z
        return Vector3(x, y, z)
    def lookAt(self, target, up):
        up = up.direction()

        look = (target - self.translation).direction()
        if look.dot(up) > 0.99:
            up = Vector3.unitX
            if look.dot(up) > 0.99:
                up = Vector3.unitY

        up -= look * look.dot(up)
        up.unitize()

        z = -look
        x = -z.cross(up)
        x.unitize()

        y = z.cross(x)

        self.rotation.setColumn(0, x)
        self.rotation.setColumn(1, y)
        self.rotation.setColumn(2, z)
    @staticmethod
    def CreateEmpty():
        return CoordinateFrame(Matrix3.CreateEmpty(), Vector3(0, 0, 0))
    @staticmethod
    def FromXML(elem):
        return CoordinateFrame(Matrix3.FromXML(elem), Vector3.FromXML(elem))
CoordinateFrame.IDENTITY = CoordinateFrame(Matrix3.IDENTITY, Vector3.ZERO)