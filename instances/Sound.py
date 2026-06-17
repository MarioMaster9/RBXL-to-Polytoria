from .Dynamic import Dynamic
from data_types import Vector3
from enums import SoundAttenuationModeEnum
class Sound(Dynamic):
    ClassName = "Sound"
    Properties = {
        "Audio": "resourceref",
        "Volume": "float",
        "Pitch": "float",
        "Autoplay": "boolean",
        "Loop": "boolean",
        "LoopStart": "float",
        "PlayInWorld": "boolean",
        "Paused": "boolean",
        "MaxDistance": "float",
        "AttenuationMode": "int"
    }
    def __init__(self):
        super().__init__()
        self.addProperties(Sound.Properties)
        self.MaxDistance = 60
        self.Autoplay = False
        self.LoopStart = 0
        self.AttenuationMode = SoundAttenuationModeEnum.Disabled
        self.LocalPosition = Vector3.ZERO
        self.LocalRotation = Vector3.ZERO