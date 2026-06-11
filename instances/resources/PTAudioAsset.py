from .AudioAsset import AudioAsset

class PTAudioAsset(AudioAsset):
    ClassName = "PTAudioAsset"
    Properties = [
        ["AudioID", "int"],
    ]
    def __init__(self):
        super().__init__()
        self.addProperties(PTAudioAsset.Properties)