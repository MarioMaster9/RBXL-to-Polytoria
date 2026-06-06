from .RigidBody import RigidBody
from rbxl.data_types import Color4
class Entity(RigidBody):
    ClassName = "Entity"
    Properties = [
        ["Color", "color"],
        ["CastShadows", "boolean"],
        ["IsSpawn", "boolean"],
    ]
    def __init__(self):
        super().__init__()
        self.addProperties(Entity.Properties)
        self.Color = Color4.WHITE
        self.IsSpawn = False