from .Instance import Instance
from .resources.PTImageAsset import PTImageAsset
from .resources.PTAudioAsset import PTAudioAsset
from .resources.PTMeshAsset import PTMeshAsset
from .resources.BuiltInFontAsset import BuiltInFontAsset


class Game(Instance):
    ClassName = "Game"
    def __init__(self, version):
        super().__init__()
        self.Version = version
        self.nonInstanceObjects = []
    def newImage(self, imageID):
        newAsset = PTImageAsset()
        newAsset.ImageID = int(imageID)
        return newAsset
    def newAudio(self, audioID):
        newAsset = PTAudioAsset()
        newAsset.AudioID = int(audioID)
        return newAsset
    def newMesh(self, assetID):
        newAsset = PTMeshAsset()
        newAsset.AssetID = int(assetID)
        return newAsset
    def newFont(self, fontPreset, fontWeight, fontStyle):
        newAsset = BuiltInFontAsset()
        newAsset.FontPreset = fontPreset
        newAsset.FontWeight = fontWeight
        newAsset.FontStyle = fontStyle
        return newAsset
    def json(self):
        json_self = {
            "Version": self.Version,
            "FileType": 0,
            "Objects": [],
            "NonInstanceObjects": []
        }
        for obj in self.children:
            json_self["Objects"].append(obj.json(self))
        for obj in self.nonInstanceObjects:
            json_self["NonInstanceObjects"].append(obj.json(self))
        return json_self
