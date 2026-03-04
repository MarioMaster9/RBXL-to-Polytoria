from .Part import Part
from enums.CollisionType import CollisionType

class MeshPart(Part):
    ClassName = "MeshPart"
    Properties = [
        ["AssetId", "int"],
        ["CollisionType", "int"],
        ["PlayAnimationOnStart", "boolean"],
    ]
    def __init__(self):
        super().__init__()
        self.addProperties(MeshPart.Properties)
        self.CollisionType = CollisionType.Bounds
        self.PlayAnimationOnStart = False