from .Sky import Sky
from enums import TextureFilterEnum
class ImageSky(Sky):
    ClassName = "ImageSky"
    Properties = [
        ["TopImage", "resourceref"],
        ["BottomImage", "resourceref"],
        ["LeftImage", "resourceref"],
        ["RightImage", "resourceref"],
        ["FrontImage", "resourceref"],
        ["BackImage", "resourceref"],
        ["TextureFilter", "int"],
    ]
    def __init__(self):
        super().__init__()
        self.addProperties(ImageSky.Properties)
        self.Name = "ImageSky"
        self.TextureFilter = TextureFilterEnum.Linear