from .Instance import Instance
class ImageSky(Instance):
    ClassName = "ImageSky"
    Properties = [
        ["TopImage", "ref"],
        ["BottomImage", "ref"],
        ["LeftImage", "ref"],
        ["RightImage", "ref"],
        ["FrontImage", "ref"],
        ["BackImage", "ref"],
    ]
    def __init__(self):
        super().__init__()
        self.addProperties(ImageSky.Properties)
        self.Name = "ImageSky"