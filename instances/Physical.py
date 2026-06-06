from .Dynamic import Dynamic
from rbxl.data_types import Vector3
class Physical(Dynamic):
    ClassName = "Physical"
    Properties = [
        ["Anchored", "boolean"],
        ["CanCollide", "boolean"],
        ["CollisionLayers", "uint"],
        ["CollisionMask", "uint"],

    ]
    def __init__(self):
        super().__init__()
        self.addProperties(Physical.Properties)
        self.Anchored = True
        self.CanCollide = True
        self.CollisionLayers = 1
        self.CollisionMask = 1