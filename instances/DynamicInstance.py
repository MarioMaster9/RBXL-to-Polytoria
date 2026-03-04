from .Instance import Instance

class DynamicInstance(Instance):
    ClassName = "DynamicInstance"
    Properties = [
        ["Position", "vector3"],
        ["Rotation", "vector3"],
        ["LocalPosition", "vector3"],
        ["LocalRotation", "vector3"],
        ["Size", "vector3"],
        ["LocalSize", "vector3"],
    ]
    def __init__(self):
        super().__init__()
        self.addProperties(DynamicInstance.Properties)