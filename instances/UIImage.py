from .UIField import UIField
class UIImage(UIField):
    ClassName = "UIImage"
    Properties = [
        ["Color", "color"],
        ["Image", "ref"],
        ["Clickable", "boolean"],
    ]
    def __init__(self):
        super().__init__()
        self.addProperties(UIImage.Properties)