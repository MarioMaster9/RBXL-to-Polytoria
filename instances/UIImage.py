from .UIField import UIField
from enums import ImageStretchModeEnum
class UIImage(UIField):
    ClassName = "UIImage"
    Properties = [
        ["Image", "ref"],
        ["TextureScale", "vector2"],
        ["TextureOffset", "vector2"],
        ["Color", "color"],
        ["StretchMode", "int"],
        ["TextureFilter", "int"], # TODO
        ["FlipHorizontal", "boolean"],
        ["FlipVertical", "boolean"],
    ]
    def __init__(self):
        super().__init__()
        self.addProperties(UIImage.Properties)
        self.FlipHorizontal = False
        self.FlipVertical = False
        self.StretchMode = ImageStretchModeEnum.Stretch