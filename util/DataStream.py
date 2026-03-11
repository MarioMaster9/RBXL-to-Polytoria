import struct

def rotation_value(value, rotations, width=32):
    """ Return a given number of bitwise left or right rotations of an integer 
    value,
    for a given bit field width.
    if rotations == -rotations:
        left
    else:
        right
    """
    if int(rotations) != abs(int(rotations)):
        rotations = width + int(rotations)
    return (int(value)<<(width-(rotations%width)) | (int(value)>>(rotations%width))) & ((1<<width)-1)

def convertInt(v, newF):
    return struct.unpack(newF, struct.pack('I', v))[0]
def convertLong(v, newF):
    return struct.unpack(newF, struct.pack('Q', v))[0]

def nothing(buffer, startIndex):
    value = int.from_bytes(buffer, 'little', signed=False)
    return value

class DataStream:
    def __init__(self,stream):
        self.stream = stream
    def readByte(self):
        return self.stream.read(1)
    def skip(self, amount):
        self.stream.read(amount)
    def tell(self):
        return self.stream.tell()
    def eof(self):
        return self.tell() > len(self.stream)
    def readBytes(self, size):
        return self.stream.read(size)
    def peek(self, size):
        data = self.stream.read(size)
        self.seek(-size, True)
        return data
    def readChars(self, size):
        stringBytes = self.readBytes(size)
        decoded = None
        try:
            decoded = stringBytes.decode('utf-8')
        except UnicodeDecodeError:
            decoded = stringBytes
        return decoded
    def readUint8(self, endianness='little'):
        return int.from_bytes(self.stream.read(1), endianness, signed=False)
    def readUint16(self, endianness='little'):
        return int.from_bytes(self.stream.read(2), endianness, signed=False)
    def readInt16(self, endianness='little'):
        return int.from_bytes(self.stream.read(2), endianness, signed=True)
    def readUint32(self, endianness='little'):
        return int.from_bytes(self.stream.read(4), endianness, signed=False)
    def readInt32(self, endianness='little'):
        return int.from_bytes(self.stream.read(4), endianness, signed=True)
    def readUint64(self, endianness='little'):
        return int.from_bytes(self.stream.read(8), endianness, signed=False)
    def readBoolean(self):
        return self.readByte() == b'\x01'
    def readLengthPrefixedString(self):
        return self.readChars(self.readUint32())
    def readString(self):
        return self.readLengthPrefixedString()
    def compare(self, data):
        return self.readBytes(len(data)) == data
    def seek(self, amt, relative=False):
        if relative:
            self.stream.seek(amt + self.tell())
        else:
            self.stream.seek(amt)
    def readRFloat32(self):
        value = rotation_value(self.readUint32('big'), 1)
        return convertInt(value, 'f')
    def readFloat32(self):
        return convertInt(self.readUint32(), 'f')
    def readFloat64(self):
        return convertLong(self.readUint64(), 'd')
    def readInterleaved(self, count, transform, dataSize):
        blobSize = count * dataSize
        
        blob = self.readBytes(blobSize)
        work = bytearray(dataSize)
        values = [None] * count
        
        for offset in range(0, count):
            for i in range(0, dataSize):
                index = (i * count) + offset
                work[dataSize - i - 1] = blob[index]
            values[offset] = transform(bytes(work), 0)
        return values
    def rotateInt64(self, buffer, startIndex):
        value = int.from_bytes(buffer[0:8], 'little', signed=True)
        return ((value&0xFFFFFFFFFFFFFFFF) >> 1) ^ (-(value & 1))
    def rotateInt32(self, buffer, startIndex):
        value = int.from_bytes(buffer[0:4], 'little', signed=True)
        return ((value&0xFFFFFFFF) >> 1) ^ (-(value & 1))
    def rotateFloat(self, buffer, startIndex):
        u = int.from_bytes(buffer[startIndex:startIndex+4], 'little', signed=False)
        i = ((u >> 1) | (u << 31))&0xFFFFFFFF
        return convertInt(i, 'f')
    def readInterleavedUint32(self, count, transform=nothing):
        return self.readInterleaved(count, transform, 4)
    def readInterleavedInt(self, count):
        result = self.readInterleavedUint32(count, self.rotateInt32)
        return result
    def readIds(self, count):
        result = self.readInterleavedInt(count)
        for i in range(1, len(result)):
            result[i] += result[i - 1]
        return result
    def readInterleavedFloat(self, count):
        result = self.readInterleaved(count, self.rotateFloat, 4)
        return result
