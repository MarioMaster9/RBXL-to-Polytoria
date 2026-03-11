from .UIField import UIField
from enums import ImageType
class UIImage(UIField):
    ClassName = "UIImage"
    Properties = [
        ["Color", "color"],
        ["ImageID", "string"],
        ["ImageType", "int"],
        ["Clickable", "boolean"],
    ]
    def __init__(self):
        super().__init__()
        self.addProperties(UIImage.Properties)
        self.ImageType = ImageType.Asset