from .UIField import UIField
from enums import ImageStretchModeEnum
from enums import TextureFilterEnum
class UIImage(UIField):
    ClassName = "UIImage"
    Properties = {
        "Image": "resourceref",
        "TextureScale": "vector2",
        "TextureOffset": "vector2",
        "Color": "color",
        "StretchMode": "int",
        "TextureFilter": "int",
        "FlipHorizontal": "boolean",
        "FlipVertical": "boolean",
    }
    def __init__(self):
        super().__init__()
        self.addProperties(UIImage.Properties)
        self.FlipHorizontal = False
        self.FlipVertical = False
        self.StretchMode = ImageStretchModeEnum.Stretch
        self.TextureFilter = TextureFilterEnum.Linear
        self.FlipHorizontal = False
        self.FlipVertical = False