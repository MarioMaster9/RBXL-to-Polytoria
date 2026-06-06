from .Instance import Instance
from .assetObjects.PTImageAsset import PTImageAsset
from .assetObjects.PTAudioAsset import PTAudioAsset
from .assetObjects.BuiltInFontAsset import BuiltInFontAsset


class Game(Instance):
    ClassName = "Game"
    def __init__(self, version):
        super().__init__()
        self.Version = version
        self.nonInstanceObjects = []
    def newImage(self, imageID):
        newAsset = PTImageAsset()
        newAsset.ImageID = int(imageID)
        self.nonInstanceObjects.append(newAsset)
        return newAsset
    def newAudio(self, audioID):
        newAsset = PTAudioAsset()
        newAsset.AudioID = int(audioID)
        self.nonInstanceObjects.append(newAsset)
        return newAsset
    def newFont(self, fontPreset, fontWeight, fontStyle):
        newAsset = BuiltInFontAsset()
        newAsset.FontPreset = fontPreset
        newAsset.FontWeight = fontWeight
        newAsset.FontStyle = fontStyle
        self.nonInstanceObjects.append(newAsset)
        return newAsset
    def json(self):
        json_self = {
            "Version": self.Version,
            "FileType": 0,
            "Objects": [],
            "NonInstanceObjects": []
        }
        for obj in self.children:
            json_self["Objects"].append(obj.json())
        for obj in self.nonInstanceObjects:
            json_self["NonInstanceObjects"].append(obj.json())
        return json_self
