import math
from .Vector3 import Vector3
halfPi = math.pi / 2

class Matrix3:
    def __init__(self, fEntry00, fEntry01, fEntry02, fEntry10, fEntry11, fEntry12, fEntry20, fEntry21, fEntry22):
        self.elt = [[fEntry00, fEntry01, fEntry02], [fEntry10, fEntry11, fEntry12], [fEntry20, fEntry21, fEntry22]]
    def __iter__(self):
        return iter((self.elt[0][0], self.elt[0][1], self.elt[0][2], self.elt[1][0], self.elt[1][1], self.elt[1][2], self.elt[2][0], self.elt[2][1], self.elt[2][2]))
    def copy(self):
        return Matrix3(*self)
    def toEulerAnglesXYZ(self, rfAngle):
        if self.elt[0][2] < 1:
            if self.elt[0][2] > -1:
                rfAngle[0] = math.atan2(-self.elt[1][2], self.elt[2][2])
                rfAngle[1] = math.asin(self.elt[0][2])
                rfAngle[2] = math.atan2( -self.elt[0][1], self.elt[0][0])
                return True
            else:
                # WARNING.  Not unique.  XA - ZA = -atan2(r10,r11)
                rfAngle[0] = -math.atan2(self.elt[1][0], self.elt[1][1])
                rfAngle[1] = -halfPi
                rfAngle[2] = 0
                return False
        else:
            # WARNING.  Not unique.  XAngle + ZAngle = atan2(r10,r11)
            rfAngle[0] = math.atan2(self.elt[1][0], self.elt[1][1])
            rfAngle[1] = halfPi
            rfAngle[2] = 0
            return False
    def toEulerAnglesYXZ(self):        
        if self.elt[1][2] < 1:
            if self.elt[1][2] > -1:
                rfYAngle = math.atan2(self.elt[0][2], self.elt[2][2])
                rfXAngle = math.asin(-self.elt[1][2])
                rfZAngle = math.atan2(self.elt[1][0], self.elt[1][1])
                return rfYAngle, rfXAngle, rfZAngle
            else:
                rfYAngle = math.atan2(self.elt[0][1], self.elt[0][0])
                rfXAngle = halfPi
                rfZAngle = 0
                return rfYAngle, rfXAngle, rfZAngle
        else:
            rfYAngle = math.atan2(-self.elt[0][1], self.elt[0][0])
            rfXAngle = -halfPi
            rfZAngle = 0
            return rfYAngle, rfXAngle, rfZAngle
    def __mul__(self, rkMatrix):
        if type(rkMatrix) is Vector3:
            kProd = Vector3(0, 0, 0)
            v = rkMatrix

            kProd.x = self.elt[0][0] * v.x + self.elt[0][1] * v.y + self.elt[0][2] * v.z
            kProd.y = self.elt[1][0] * v.x + self.elt[1][1] * v.y + self.elt[1][2] * v.z
            kProd.z = self.elt[2][0] * v.x + self.elt[2][1] * v.y + self.elt[2][2] * v.z

            return kProd
        if rkMatrix is None:
            return self
        kProd = Matrix3.CreateEmpty()
        kProd.elt[0][0] = self.elt[0][0] * rkMatrix.elt[0][0] + self.elt[0][1] * rkMatrix.elt[1][0] + self.elt[0][2] * rkMatrix.elt[2][0]
        kProd.elt[0][1] = self.elt[0][0] * rkMatrix.elt[0][1] + self.elt[0][1] * rkMatrix.elt[1][1] + self.elt[0][2] * rkMatrix.elt[2][1]
        kProd.elt[0][2] = self.elt[0][0] * rkMatrix.elt[0][2] + self.elt[0][1] * rkMatrix.elt[1][2] + self.elt[0][2] * rkMatrix.elt[2][2]
        
        kProd.elt[1][0] = self.elt[1][0] * rkMatrix.elt[0][0] + self.elt[1][1] * rkMatrix.elt[1][0] + self.elt[1][2] * rkMatrix.elt[2][0]
        kProd.elt[1][1] = self.elt[1][0] * rkMatrix.elt[0][1] + self.elt[1][1] * rkMatrix.elt[1][1] + self.elt[1][2] * rkMatrix.elt[2][1]
        kProd.elt[1][2] = self.elt[1][0] * rkMatrix.elt[0][2] + self.elt[1][1] * rkMatrix.elt[1][2] + self.elt[1][2] * rkMatrix.elt[2][2]
        
        kProd.elt[2][0] = self.elt[2][0] * rkMatrix.elt[0][0] + self.elt[2][1] * rkMatrix.elt[1][0] + self.elt[2][2] * rkMatrix.elt[2][0]
        kProd.elt[2][1] = self.elt[2][0] * rkMatrix.elt[0][1] + self.elt[2][1] * rkMatrix.elt[1][1] + self.elt[2][2] * rkMatrix.elt[2][1]
        kProd.elt[2][2] = self.elt[2][0] * rkMatrix.elt[0][2] + self.elt[2][1] * rkMatrix.elt[1][2] + self.elt[2][2] * rkMatrix.elt[2][2]
        return kProd
    def setColumn(self, iCol, vector):
        self.elt[0][iCol] = vector.x
        self.elt[1][iCol] = vector.y
        self.elt[2][iCol] = vector.z
    def orthonormalize(self):
        # Algorithm uses Gram-Schmidt orthogonalization.  If 'this' matrix is
        # M = [m0|m1|m2], then orthonormal output matrix is Q = [q0|q1|q2],
        #
        #   q0 = m0/|m0|
        #   q1 = (m1-(q0*m1)q0)/|m1-(q0*m1)q0|
        #   q2 = (m2-(q0*m2)q0-(q1*m2)q1)/|m2-(q0*m2)q0-(q1*m2)q1|
        #
        # where |V| indicates length of vector V and A*B indicates dot
        # product of vectors A and B.

        # compute q0
        fInvLength = 1 / math.sqrt(self.elt[0][0] * self.elt[0][0] + self.elt[1][0] * self.elt[1][0] + self.elt[2][0] * self.elt[2][0])

        self.elt[0][0] *= fInvLength
        self.elt[1][0] *= fInvLength
        self.elt[2][0] *= fInvLength

        # compute q1
        fDot0 = self.elt[0][0] * self.elt[0][1] + self.elt[1][0] * self.elt[1][1] + self.elt[2][0] * self.elt[2][1]

        self.elt[0][1] -= fDot0 * self.elt[0][0]
        self.elt[1][1] -= fDot0 * self.elt[1][0]
        self.elt[2][1] -= fDot0 * self.elt[2][0]

        fInvLength = 1 / math.sqrt(self.elt[0][1] * self.elt[0][1] + self.elt[1][1] * self.elt[1][1] + self.elt[2][1] * self.elt[2][1])

        self.elt[0][1] *= fInvLength
        self.elt[1][1] *= fInvLength
        self.elt[2][1] *= fInvLength

        # compute q2
        fDot1 = self.elt[0][1] * self.elt[0][2] + self.elt[1][1] * self.elt[1][2] + self.elt[2][1] * self.elt[2][2]

        fDot0 = self.elt[0][0] * self.elt[0][2] + self.elt[1][0] * self.elt[1][2] + self.elt[2][0] * self.elt[2][2]

        self.elt[0][2] -= fDot0 * self.elt[0][0] + fDot1 * self.elt[0][1]
        self.elt[1][2] -= fDot0 * self.elt[1][0] + fDot1 * self.elt[1][1]
        self.elt[2][2] -= fDot0 * self.elt[2][0] + fDot1 * self.elt[2][1]

        fInvLength = 1 / math.sqrt(self.elt[0][2] * self.elt[0][2] + self.elt[1][2] * self.elt[1][2] + self.elt[2][2] * self.elt[2][2])

        self.elt[0][2] *= fInvLength
        self.elt[1][2] *= fInvLength
        self.elt[2][2] *= fInvLength
    @staticmethod
    def fromEulerAnglesYXZ(fYAngle, fPAngle, fRAngle):
        fCos = math.cos(fYAngle)
        fSin = math.sin(fYAngle)
        kYMat = Matrix3(fCos, 0, fSin, 0, 1, 0, -fSin, 0, fCos)

        fCos = math.cos(fPAngle)
        fSin = math.sin(fPAngle)
        kXMat = Matrix3(1, 0, 0, 0, fCos, -fSin, 0, fSin, fCos)

        fCos = math.cos(fRAngle)
        fSin = math.sin(fRAngle)
        kZMat = Matrix3(fCos, -fSin, 0, fSin, fCos, 0, 0, 0, 1)

        return kYMat * (kXMat * kZMat)
    @staticmethod
    def fromEulerAnglesXYZ(fYAngle, fPAngle, fRAngle):
        fCos = math.cos(fYAngle)
        fSin = math.sin(fYAngle)
        kXMat = Matrix3(1.0, 0.0, 0.0, 0.0, fCos, -fSin, 0.0, fSin, fCos)

        fCos = math.cos(fPAngle)
        fSin = math.sin(fPAngle)
        kYMat = Matrix3(fCos, 0.0, fSin, 0.0, 1.0, 0.0, -fSin, 0.0, fCos)

        fCos = math.cos(fRAngle)
        fSin = math.sin(fRAngle)
        kZMat = Matrix3(fCos, -fSin, 0.0, fSin, fCos, 0.0, 0.0, 0.0, 1.0)

        return kXMat * (kYMat * kZMat)
    @staticmethod
    def fromAxisAngle(rkAxis, fRadians):
        m = Matrix3.CreateEmpty()
        
        fCos = math.cos(fRadians)
        fSin = math.sin(fRadians)
        fOneMinusCos = 1.0 - fCos
        fX2 = rkAxis.x * rkAxis.x
        fY2 = rkAxis.y * rkAxis.y
        fZ2 = rkAxis.z * rkAxis.z
        fXYM = rkAxis.x * rkAxis.y * fOneMinusCos
        fXZM = rkAxis.x * rkAxis.z * fOneMinusCos
        fYZM = rkAxis.y * rkAxis.z * fOneMinusCos
        fXSin = rkAxis.x * fSin
        fYSin = rkAxis.y * fSin
        fZSin = rkAxis.z * fSin

        m.elt[0][0] = fX2 * fOneMinusCos + fCos
        m.elt[0][1] = fXYM - fZSin
        m.elt[0][2] = fXZM + fYSin
        m.elt[1][0] = fXYM + fZSin
        m.elt[1][1] = fY2 * fOneMinusCos + fCos
        m.elt[1][2] = fYZM - fXSin
        m.elt[2][0] = fXZM - fYSin
        m.elt[2][1] = fYZM + fXSin
        m.elt[2][2] = fZ2 * fOneMinusCos + fCos

        return m
    @staticmethod
    def CreateEmpty():
        return Matrix3(0, 0, 0, 0, 0, 0, 0, 0, 0)
    @staticmethod
    def FromXML(elem):
        r00 = float(elem.find("R00").text)
        r01 = float(elem.find("R01").text)
        r02 = float(elem.find("R02").text)
        r10 = float(elem.find("R10").text)
        r11 = float(elem.find("R11").text)
        r12 = float(elem.find("R12").text)
        r20 = float(elem.find("R20").text)
        r21 = float(elem.find("R21").text)
        r22 = float(elem.find("R22").text)
        return Matrix3(r00, r01, r02, r10, r11, r12, r20, r21, r22)
Matrix3.IDENTITY = Matrix3(1, 0, 0, 0, 1, 0, 0, 0, 1)