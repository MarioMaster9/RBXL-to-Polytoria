from .Instance import Instance
from enums import AmbientSourceEnum, SkyboxEnum
from data_types import Color
class Lighting(Instance):
    ClassName = "Lighting"
    Properties = [
        ["Skybox", "int"],
        ["AmbientSource", "int"],
        ["AmbientColor", "color"],
        ["FogEnabled", "boolean"],
        ["FogColor", "color"],
        ["FogStartDistance", "float"],
        ["FogEndDistance", "float"],
    ]
    def __init__(self):
        super().__init__()
        self.addProperties(Lighting.Properties)
        self.Skybox = SkyboxEnum.Day1
        self.AmbientSource = AmbientSourceEnum.Color
        self.FogEnabled = False
        self.FogColor = Color(1, 1, 1)
        self.FogStartDistance = 0
        self.FogEndDistance = 0
        self.Name = "Lighting"