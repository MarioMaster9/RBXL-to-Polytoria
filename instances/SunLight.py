from .Light import Light
from rbxl.data_types import Vector3
class SunLight(Light):
    ClassName = "SunLight"
    def __init__(self):
        super().__init__()
        self.Position = Vector3(0, 15, 0)
        self.Size = Vector3.ONE
        self.Shadows = True
        self.Name = "SunLight"