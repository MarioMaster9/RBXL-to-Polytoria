from .Instance import Instance
from data_types import Vector3
class Environment(Instance):
    ClassName = "Environment"
    Properties = {
        "Gravity": "vector3",
        "PartDestroyHeight": "float",
        "AutoGenerateNavMesh": "boolean",
    }
    def __init__(self):
        super().__init__()
        self.addProperties(Environment.Properties)
        self.Gravity = Vector3(0, -85, 0)
        self.PartDestroyHeight = -2000.0
        self.AutoGenerateNavMesh = False
        self.Name = "Environment"