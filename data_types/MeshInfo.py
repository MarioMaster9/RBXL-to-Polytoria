from .Content import Content
from .Vector3 import Vector3

class MeshInfo:
    def __init__(self, _type, id, offset, scale, vertexColor, exists=True):
        self.type = _type
        self.id = id
        self.offset = offset
        self.scale = scale
        self.vertexColor = vertexColor
        self.exists = exists
MeshInfo.EMPTY = MeshInfo("", Content.EMPTY, Vector3.ZERO, Vector3.ONE, Vector3.ONE, False)