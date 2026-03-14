from .DynamicInstance import DynamicInstance
from rbxl.data_types import Color4, Vector3
class SunLight(DynamicInstance):
    ClassName = "SunLight"
    Properties = [
        ["Brightness", "float"],
        ["Color", "color"],
        ["Shadows", "boolean"],
    ]
    def __init__(self):
        super().__init__()
        self.addProperties(SunLight.Properties)
        self.Position = Vector3(0, 15, 0)
        self.Size = Vector3.ONE
        self.Shadows = True
        self.Name = "SunLight"