from .Entity import Entity
from enums import CollisionTypeEnum
from enums import TextureFilterEnum
class Mesh(Entity):
    ClassName = "Mesh"
    Properties = [
        ["Asset", "resourceref"],
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
        self.IncludeOffset = False
        self.CollisionType = CollisionTypeEnum.Bounds
        self.TextureFilter = TextureFilterEnum.Linear
        self.PlayAnimationOnStart = False
        self.UsePartColor = False
        self.CastShadows = True
