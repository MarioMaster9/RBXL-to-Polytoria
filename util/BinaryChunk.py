import struct
import lz4.frame
import zstd as zstd

from .BinaryTreeItem import BinaryTreeItem
from .BinaryToken import BinaryToken

from data_types import *

intConvert = lambda x, a: struct.unpack('<i', x)[0]
uintConvert = lambda x, a: struct.unpack('<I', x)[0]
uint64Convert = lambda x, a: struct.unpack('<Q', x)[0]


magic = b'\x04\x22\x4D\x18'
framedescriptor = b'\x60\x70\x73'
headerstart = magic + framedescriptor

def createFrame(fp, length):
    header = headerstart + length.to_bytes(4, 'little')
    data = header + fp.readBytes(length)
    return data + b'\x00\x00\x00\x00'

zstdheader = b'\x28\xB5\x2F\xFD'

def decompress(stream):
    comLength = stream.readUint32()
    decomLength = stream.readUint32()
    reserved = stream.readUint32()

    if comLength == 0:
        return stream.readBytes(decomLength)
    
    if comLength > 4 and stream.peek(4) == zstdheader:
        return zstd.decompress(stream.readBytes(comLength))
    else:
        return lz4.frame.decompress(createFrame(stream, comLength))
class BinaryChunk:
    def __init__(self, stream):
        self.loadFromFile(stream)
    def loadFromFile(self, stream):
        self.signature = stream.readBytes(4)
        self.payload = decompress(stream)
    def uniqueDecode(self, stream, rbxl):
        match self.signature:
            case b'INST':
                self.decode_INST(stream, rbxl)
            case b'PROP':
                self.decode_PROP(stream, rbxl)
            case b'PRNT':
                self.decode_PRNT(stream, rbxl)
            case b'SSTR':
                self.decode_SSTR(stream, rbxl)
            case b'HASH':
                self.decode_HASH(stream, rbxl)
            case _:
                print(self.signature)
    def decode_INST(self, stream, rbxl):
        self.classID = stream.readInt32()
        rbxl.classes[self.classID] = self
        self.className = stream.readLengthPrefixedString()
        self.hasService = stream.readBoolean()
        self.length = stream.readUint32()
        self.ids = self.readReferences(stream, self.length, rbxl)
        for ref in self.ids:
            refId = ref[1]
            rbxl.instances[refId] = BinaryTreeItem(self.className)
    def decode_PROP(self, stream, rbxl):
        self.classID = stream.readInt32()
        self.name = stream.readString()
        
        _class = rbxl.classes[self.classID]
        
        self.values = self.readProperties(stream, _class.length, rbxl)
        for i, ref in enumerate(_class.ids):
            refId = ref[1]
            rbxl.instances[refId].properties[self.name] = self.values[i]
    def decode_PRNT(self, stream, rbxl):
        version = stream.readUint8()
        assert version == 0, "PRNT version mismatch"
        self.length = stream.readInt32()
        self.childIds = stream.readIds(self.length)
        self.parentIds = stream.readIds(self.length)
        
        for i in range(0, self.length):
            child = rbxl.instances[self.childIds[i]]
            parent = rbxl.instances[self.parentIds[i]]
            parent.addChild(child)
    def decode_SSTR(self, stream, rbxl):
        self.version = stream.readUint32()
        assert self.version == 0, f'Invalid SharedString Chunk Version! Expected 0, got {self.version}'
        
        self.count = stream.readUint32()
        for i in range(0, self.count):
            md5 = stream.readBytes(16).hex()
            value = stream.readString()
            rbxl.sharedStrings.append({"md5": md5, "value": value})
    def decode_HASH(self, stream, rbxl):
        self.instanceCount = stream.readUint32()
        self.hashSize = stream.readUint8()
        self.hashFunc = stream.readUint8()
        self.data = []
        for i in range(self.instanceCount):
            item = stream.readBytes(self.hashSize).hex()
            self.data.append(item)
    def readReferences(self, stream, instCount, rbxl):
        values = stream.readIds(instCount)
        refIds = []
        for value in values:
            refIds.append(["REF", value])
        return refIds
    def readProperties(self, stream, instCount, rbxl=None):
        tokenId = stream.readUint8()
        return self.readTyped(tokenId, stream, instCount, rbxl)
    def readTyped(self, tokenId, stream, instCount, rbxl=None):
        values = []
        match tokenId:
            case BinaryToken.STRING:
                for i in range(instCount):
                    values.append(stream.readString())
            case BinaryToken.BOOLEAN:
                for i in range(instCount):
                    values.append(stream.readBoolean())
            case BinaryToken.INT32:
                values = stream.readInterleavedInt(instCount)
            case BinaryToken.FLOAT32:
                values = stream.readInterleavedFloat(instCount)
            case BinaryToken.FLOAT64:
                for i in range(instCount):
                    values.append(stream.readFloat64())
            case BinaryToken.UDIM:
                scale = stream.readInterleavedFloat(instCount)
                off = stream.readInterleavedInt(instCount)
                for i in range(instCount):
                    values.append(UDim(scale[i], off[i]))
            case BinaryToken.UDIM2:
                scaleX = stream.readInterleavedFloat(instCount)
                scaleY = stream.readInterleavedFloat(instCount)
                offX = stream.readInterleavedInt(instCount)
                offY = stream.readInterleavedInt(instCount)
                for i in range(instCount):
                    values.append(UDim2(Vector2(scaleX[i], scaleY[i]), Vector2(offX[i], offY[i])))
            case BinaryToken.RAY:
                for i in range(instCount):
                    pos = [stream.readFloat32() for _ in range(3)]
                    dir = [stream.readFloat32() for _ in range(3)]
                    values.append({'origin': Vector3(*pos), 'direction': Vector3(*dir)})
            case BinaryToken.FACES:
                for i in range(instCount):
                    values.append(stream.readUint8())
            case BinaryToken.AXES:
                for i in range(instCount):
                    values.append(stream.readUint8())
            case BinaryToken.BRICKCOLOR:
                values = stream.readInterleaved(instCount, intConvert, 4)
            case BinaryToken.COLOR3:
                r = stream.readInterleavedFloat(instCount)
                g = stream.readInterleavedFloat(instCount)
                b = stream.readInterleavedFloat(instCount)
                for i in range(instCount):
                    color = Color3(r[i], g[i], b[i])
                    values.append(color)
            case BinaryToken.VECTOR2:
                x = stream.readInterleavedFloat(instCount)
                y = stream.readInterleavedFloat(instCount)
                for i in range(instCount):
                    values.append(Vector2(x[i], y[i]))
            case BinaryToken.VECTOR3:
                x = stream.readInterleavedFloat(instCount)
                y = stream.readInterleavedFloat(instCount)
                z = stream.readInterleavedFloat(instCount)
                for i in range(instCount):
                    values.append(Vector3(x[i], y[i], z[i]))
            case BinaryToken.VECTOR2INT16:
                for i in range(instCount):
                    x = stream.readInt16()
                    y = stream.readInt16()
                    values.append(Vector2(x, y))
            case BinaryToken.CFRAME:
                matrices = []
                for i in range(instCount):
                    orientId = stream.readUint8()
                    matrix = None
                    if orientId == 0:
                        transform = [stream.readFloat32() for _ in range(9)]
                        matrix = Matrix3(*transform)
                    else:
                        matrix = Matrix3.FromOrientId(orientId - 1)
                    matrices.append(matrix)
                positions = self.readTyped(BinaryToken.VECTOR3, stream, instCount)
                for i, position in enumerate(positions):
                    values.append(CoordinateFrame(matrices[i], positions[i]))
            case BinaryToken.CFRAMEQUAT:
                matrices = []
                for i in range(instCount):
                    orientId = stream.readUint8()
                    matrix = None
                    if orientId == 0:
                        quaternion = [stream.readFloat32() for _ in range(4)]
                        matrix = Quaternion(*quaternion).toRotationMatrix()
                    else:
                        matrix = Matrix3.FromOrientId(orientId - 1)
                    matrices.append(matrix)
                positions = self.readTyped(BinaryToken.VECTOR3, stream, instCount)
                for i, position in enumerate(positions):
                    values.append(CoordinateFrame(matrices[i], positions[i]))
            case BinaryToken.ENUM:
                values = stream.readInterleaved(instCount, intConvert, 4)
            case BinaryToken.REFERENT:
                values = self.readReferences(stream, instCount, rbxl)
            case BinaryToken.VECTOR3INT16:
                for i in range(instCount):
                    x = stream.readInt16()
                    y = stream.readInt16()
                    z = stream.readInt16()
                    values.append(Vector3(x, y, z))
            case BinaryToken.NUMBERSEQUENCE:
                for i in range(instCount):
                    length = stream.readUint32()
                    keypoints = []
                    for j in range(0, length):
                        time = stream.readFloat32()
                        value = stream.readFloat32()
                        envelope = stream.readFloat32()
                        keypoints.append(NumberSequenceKeypoint(time, value))
                    values.append(NumberSequence(keypoints))
            case BinaryToken.COLORSEQUENCE:
                for i in range(instCount):
                    length = stream.readUint32()
                    keypoints = []
                    for j in range(0, length):
                        time = stream.readFloat32()
                        color = Color3(stream.readFloat32(), stream.readFloat32(), stream.readFloat32())
                        envelope = stream.readFloat32()
                        keypoints.append(ColorSequenceKeypoint(time, color))
                    values.append(ColorSequence(keypoints))
            case BinaryToken.NUMBERRANGE:
                for i in range(instCount):
                    _min = stream.readFloat32()
                    _max = stream.readFloat32()
                    values.append(NumberRange(_min, _max))
            case BinaryToken.RECT:
                rectMin = self.readTyped(BinaryToken.VECTOR2, stream, instCount)
                rectMax = self.readTyped(BinaryToken.VECTOR2, stream, instCount)
                for i in range(instCount):
                    values.append(Rect(rectMin[i], rectMax[i]))
            case BinaryToken.PHYSICALPROPERTIES:
                for i in range(instCount):
                    phys = PhysicalProperties()
                    config = stream.readUint8()
                    if config & 0x1:
                        phys.Density = stream.readFloat32()
                        phys.Friction = stream.readFloat32()
                        phys.Elasticity = stream.readFloat32()
                        phys.FrictionWeight = stream.readFloat32()
                        phys.ElasticityWeight = stream.readFloat32()
                        if config & 0x2:
                            phys.AcousticAbsorption = stream.readFloat32()
                    values.append(phys)
            case BinaryToken.COLOR3UINT8:
                r = stream.readBytes(instCount)
                g = stream.readBytes(instCount)
                b = stream.readBytes(instCount)
                for i in range(instCount):
                    values.append(Color3(r[i]/255,g[i]/255,b[i]/255))
            case BinaryToken.INT64:
                values = stream.readInterleaved(instCount, stream.rotateInt64, 8)
            case BinaryToken.SHAREDSTRING:
                indices = stream.readInterleavedUint32(instCount)
                for index in indices:
                    values.append(rbxl.sharedStrings[index])
            case BinaryToken.BYTECODE:
                for i in range(instCount):
                    length = stream.readInt32()
                    values.append(stream.readBytes(length))
            case BinaryToken.OPTIONALCOORDINATEFRAME:
                cframes = self.readProperties(stream, instCount, rbxl)
                bools = self.readProperties(stream, instCount, rbxl)
                for i in range(instCount):
                    if bools[i] == False:
                        cframes[i] = None
                values = cframes
            case BinaryToken.UNIQUEID:
                def transform(buffer, offset):
                    random = stream.rotateInt64(buffer, 0)
                    _time = uintConvert(buffer[8:12], 0)
                    _index = uintConvert(buffer[12:16], 0)
                    v = [random, _time, _index]
                    return v
                values = stream.readInterleaved(instCount, transform, 16)
            case BinaryToken.FONT:
                for i in range(instCount):
                    family = Content(stream.readString())
                    weight = stream.readUint16()
                    style = stream.readUint8() and "Italic" or "Normal"
                    cachedFaceId = Content(stream.readString())
                    values.append(FontFace(family, weight, style))
            case BinaryToken.CAPABILITIES:
                values = stream.readInterleaved(instCount, uint64Convert, 8)
            case _:
                raise NotImplementedError(f'UNSUPPORTED TOKEN: {hex(tokenId)}')
        return values