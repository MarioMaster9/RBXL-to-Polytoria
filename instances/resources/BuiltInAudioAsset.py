from .AudioAsset import AudioAsset

class BuiltInAudioAsset(AudioAsset):
    ClassName = "BuiltInAudioAsset"
    Properties = [
        ["AudioPreset", "int"]
    ]
    def __init__(self):
        super().__init__()
        self.addProperties(BuiltInAudioAsset.Properties)