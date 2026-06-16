from .Dynamic import Dynamic
from data_types import Vector3

class Light(Dynamic):
    ClassName = "Light"
    Properties = [
        ["Enabled", "boolean"],
        ["Color", "color"],
        ["Brightness", "float"],
        ["LightSize", "float"],
        ["Specular", "float"],
        ["Shadows", "boolean"],
    ]
    def __init__(self):
        super().__init__()
        self.addProperties(Light.Properties)
        self.LocalPosition = Vector3.ZERO
        self.LocalRotation = Vector3.ZERO