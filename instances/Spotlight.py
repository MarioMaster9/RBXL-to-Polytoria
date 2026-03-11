from .DynamicInstance import DynamicInstance
from data_types import Vector3
class Spotlight(DynamicInstance):
    ClassName = "Spotlight"
    Properties = [
        ["Range", "float"],
        ["Angle", "float"],
        ["Brightness", "float"],
        ["Color", "color"],
        ["Shadows", "boolean"],
    ]
    def __init__(self):
        super().__init__()
        self.addProperties(Spotlight.Properties)
        self.LocalPosition = Vector3.ZERO
        self.LocalRotation = Vector3.ZERO