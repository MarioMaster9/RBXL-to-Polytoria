from .PTImageAsset import PTImageAsset
from .PTAudioAsset import PTAudioAsset
from .PTMeshAsset import PTMeshAsset
from .BuiltInFontAsset import BuiltInFontAsset
from .BuiltInAudioAsset import BuiltInAudioAsset

class ResourceFactory:
    @staticmethod
    def CreateImage(imageID):
        newAsset = PTImageAsset()
        newAsset.ImageID = int(imageID)
        return newAsset
    @staticmethod
    def CreateAudio(audioID):
        newAsset = PTAudioAsset()
        newAsset.AudioID = int(audioID)
        return newAsset
    @staticmethod
    def CreateBuiltInAudioAsset(audioPreset):
        newAsset = BuiltInAudioAsset()
        newAsset.AudioPreset = audioPreset
        return newAsset
    @staticmethod
    def CreateMesh(assetID):
        newAsset = PTMeshAsset()
        newAsset.AssetID = int(assetID)
        return newAsset
    @staticmethod
    def CreateFont(fontPreset, fontWeight, fontStyle):
        newAsset = BuiltInFontAsset()
        newAsset.FontPreset = fontPreset
        newAsset.FontWeight = fontWeight
        newAsset.FontStyle = fontStyle
        return newAsset
