from .Dynamic import Dynamic
from rbxl.data_types import Vector3
class Sound(Dynamic):
    ClassName = "Sound"
    Properties = [
        ["Audio", "resourceref"],
        ["Volume", "float"],
        ["Pitch", "float"],
        ["Autoplay", "boolean"],
        ["Loop", "boolean"],
        ["PlayInWorld", "boolean"],
        ["Paused", "boolean"],
        ["MaxDistance", "float"],
    ]
    def __init__(self):
        super().__init__()
        self.addProperties(Sound.Properties)
        self.MaxDistance = 60
        self.Autoplay = False
        self.LocalPosition = Vector3.ZERO
        self.LocalRotation = Vector3.ZERO