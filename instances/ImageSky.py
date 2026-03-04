from .Instance import Instance

class ImageSky(Instance):
    ClassName = "ImageSky"
    Properties = [
        ["TopId", "int"],
        ["BottomId", "int"],
        ["LeftId", "int"],
        ["RightId", "int"],
        ["FrontId", "int"],
        ["BackId", "int"],
    ]
    def __init__(self):
        super().__init__()
        self.addProperties(ImageSky.Properties)
        self.Name = "ImageSky"