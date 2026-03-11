from .Content import Content
from .Vector3 import Vector3

class MeshInfo:
    def __init__(self, _type, id, textureId, offset, scale, vertexColor, exists=True):
        self.type = _type
        if type(id) is Content:
            self.id = id
        else:
            self.id = Content(id)
        if type(textureId) is Content:
            self.textureId = textureId
        else:
            self.textureId = Content(textureId)
        self.offset = offset
        self.scale = scale
        self.vertexColor = vertexColor
        self.exists = exists
MeshInfo.EMPTY = MeshInfo("", Content.EMPTY, Content.EMPTY, Vector3.ZERO, Vector3.ONE, Vector3.ONE, False)