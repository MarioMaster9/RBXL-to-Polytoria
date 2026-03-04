from .DynamicInstance import DynamicInstance
from data_types.Vector3 import Vector3

class PointLight(DynamicInstance):
    ClassName = "PointLight"
    Properties = [
        ["Range", "float"],
        ["Brightness", "float"],
        ["Color", "color"],
        ["Shadows", "boolean"],
    ]
    def __init__(self):
        super().__init__()
        self.addProperties(PointLight.Properties)
        self.LocalPosition = Vector3.ZERO
        self.LocalRotation = Vector3.ZERO