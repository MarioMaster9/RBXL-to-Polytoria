from .ImageAsset import ImageAsset
from enums import ImageType

class PTImageAsset(ImageAsset):
    ClassName = "PTImageAsset"
    Properties = [
        ["ImageID", "int"],
        ["ImageType", "int"],
    ]
    def __init__(self):
        super().__init__()
        self.addProperties(PTImageAsset.Properties)
        self.ImageType = ImageType.Asset