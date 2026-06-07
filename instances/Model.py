from .Dynamic import Dynamic
from rbxl.data_types import Vector3
class Model(Dynamic):
    ClassName = "Model"
    def __init__(self):
        super().__init__()
        self.Position = Vector3.ZERO
        self.Rotation = Vector3.ZERO
        self.Size = Vector3.ZERO