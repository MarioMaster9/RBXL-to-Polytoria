from .Instance import Instance
from enums import AmbientSourceEnum, SkyboxEnum
from rbxl.data_types import Color4
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
        self.FogStartDistance = 0
        self.FogEndDistance = 0
        self.FogColor = Color4.WHITE
        self.Name = "Lighting"