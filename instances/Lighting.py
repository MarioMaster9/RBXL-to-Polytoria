from .Instance import Instance
from enums.AmbientSource import AmbientSource

class Lighting(Instance):
    ClassName = "Lighting"
    Properties = [
        ["AmbientColor", "color"],
        ["AmbientSource", "int"],
    ]
    def __init__(self):
        super().__init__()
        self.addProperties(Lighting.Properties)
        self.AmbientSource = AmbientSource.AmbientColor
        self.Name = "Lighting"