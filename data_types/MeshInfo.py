from .Content import Content

class MeshInfo:
    def __init__(self, _type, id, exists=True):
        self.type = _type
        self.id = id
        self.exists = exists
MeshInfo.EMPTY = MeshInfo("", Content.EMPTY, False)