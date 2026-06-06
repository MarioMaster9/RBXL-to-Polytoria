from .Instance import Instance
from enums import AmbientSource, SkyboxPreset
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
        self.Skybox = SkyboxPreset.Day1
        self.AmbientSource = AmbientSource.AmbientColor
        self.FogEnabled = False
        self.FogStartDistance = 0
        self.FogEndDistance = 0
        self.FogColor = Color4.WHITE
        self.Name = "Lighting"