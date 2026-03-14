from .DynamicInstance import DynamicInstance
from rbxl.data_types import Vector3
class Sound(DynamicInstance):
    ClassName = "Sound"
    Properties = [
        ["SoundID", "string"],
        ["Pitch", "float"],
        ["MaxDistance", "float"],
        ["Autoplay", "boolean"],
        ["Loop", "boolean"],
        ["PlayInWorld", "boolean"],
        ["Volume", "float"],
    ]
    def __init__(self):
        super().__init__()
        self.addProperties(Sound.Properties)
        self.MaxDistance = 60
        self.Autoplay = False
        self.LocalPosition = Vector3.ZERO
        self.LocalRotation = Vector3.ZERO