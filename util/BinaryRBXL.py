import io
from .BinaryChunk import BinaryChunk
from .BinaryTreeItem import BinaryTreeItem
from .DataStream import DataStream

class BinaryRBXL:
    def __init__(self, stream):
        self.loadFromFile(stream)
    def loadFromFile(self, stream):
        self.root = BinaryTreeItem('')
        assert stream.compare(b'<roblox!\x89\xFF\r\n\x1A\n'), 'malformed binary header'
        self.chunks = []
        
        
        self.version = stream.readUint16()
        if self.version == 0:
            self.classCount = stream.readUint32()
            self.instanceCount = stream.readUint32()
            self.instances = {}
            self.instances[-1] = self.root # handle root parent
            self.sharedStrings = []
            stream.skip(8)
            
            self.classes = [None] * self.classCount
            self.topLevel = []
            
            # PARSE
            while True:
                chunk = self.decodeChunk(stream)
                if chunk.signature == b'END\x00':
                    break
                self.chunks.append(chunk)
            for chunk in self.chunks:
                chunk.uniqueDecode(DataStream(io.BytesIO(chunk.payload)), self)
    def decodeChunk(self, stream):
        chunk = BinaryChunk(stream)
        return chunk