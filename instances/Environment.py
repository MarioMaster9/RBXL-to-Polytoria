from .Instance import Instance
from enums import SkyboxPreset
from data_types import Vector3, Color4
class Environment(Instance):
    ClassName = "Environment"
    Properties = [
        ["Skybox", "int"],                          # MOVED IN 2.0
        ["Gravity", "vector3"],
        ["FogEnabled", "boolean"],
        ["FogStartDistance", "float"],
        ["FogEndDistance", "float"],
        ["FogColor", "color"],
        ["PartDestroyHeight", "float"],
        ["AutoGenerateNavMesh", "boolean"],
    ]
    def __init__(self):
        super().__init__()
        self.addProperties(Environment.Properties)
        self.Skybox = SkyboxPreset.Day1
        self.Gravity = Vector3(0, -85, 0)
        self.PartDestroyHeight = -2000
        self.AutoGenerateNavMesh = False
        self.FogEnabled = False
        self.FogStartDistance = 0
        self.FogEndDistance = 0
        self.FogColor = Color4.WHITE
        self.Name = "Environment"