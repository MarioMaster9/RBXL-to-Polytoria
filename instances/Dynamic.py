from .Instance import Instance
from data_types import Vector3
class Dynamic(Instance):
    ClassName = "Dynamic"
    Properties = [
        ["Position", "vector3"],
        ["Rotation", "vector3"],
        ["Size", "vector3"],
        ["LocalPosition", "vector3"],
        ["LocalRotation", "vector3"],
        ["LocalSize", "vector3"]
    ]
    def __init__(self):
        super().__init__()
        self.addProperties(Dynamic.Properties)
        #self.LocalPosition = Vector3.ZERO
        #self.LocalRotation = Vector3.ZERO
        #self.LocalSize = Vector3.ONE
        self.Position = Vector3.ZERO
        self.Rotation = Vector3.ZERO
        self.Size = Vector3.ONE
        
