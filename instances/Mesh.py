from .Entity import Entity
from enums import CollisionType
class Mesh(Entity):
    ClassName = "Mesh"
    Properties = [
        ["Asset", "ref"],
        ["IncludeOffset", "boolean"],
        ["CollisionType", "int"],
        ["TextureFilter", "int"],
        ["PlayAnimationOnStart", "boolean"],
        ["UsePartColor", "boolean"],
        ["Color", "color"],
        ["CastShadows", "boolean"],
    ]
    def __init__(self):
        super().__init__()
        self.addProperties(Mesh.Properties)
        self.CollisionType = CollisionType.Bounds
        self.PlayAnimationOnStart = False