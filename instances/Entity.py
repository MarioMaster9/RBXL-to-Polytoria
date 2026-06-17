from .RigidBody import RigidBody
from data_types import Color
class Entity(RigidBody):
    ClassName = "Entity"
    Properties = {
        "Color": "color",
        "CastShadows": "boolean",
        "IsSpawn": "boolean",
    }
    def __init__(self):
        super().__init__()
        self.addProperties(Entity.Properties)
        self.Color = Color(1, 1, 1)
        self.CastShadows = True
        self.IsSpawn = False