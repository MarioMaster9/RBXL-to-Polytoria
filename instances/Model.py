from .DynamicInstance import DynamicInstance
from data_types import Vector3
class Model(DynamicInstance):
    ClassName = "Model"
    def __init__(self):
        super().__init__()
        self.Position = Vector3.ZERO
        self.Rotation = Vector3.ZERO
        self.Size = Vector3.ZERO