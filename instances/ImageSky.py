from .Instance import Instance
class ImageSky(Instance):
    ClassName = "ImageSky"
    Properties = [
        ["TopImage", "resourceref"],
        ["BottomImage", "resourceref"],
        ["LeftImage", "resourceref"],
        ["RightImage", "resourceref"],
        ["FrontImage", "resourceref"],
        ["BackImage", "resourceref"],
    ]
    def __init__(self):
        super().__init__()
        self.addProperties(ImageSky.Properties)
        self.Name = "ImageSky"