from .UIField import UIField
class UIView(UIField):
    ClassName = "UIView"
    Properties = [
        ["BorderColor", "color"],
        ["Color", "color"],
        ["BorderWidth", "float"],
        ["CornerRadius", "float"],
    ]
    def __init__(self):
        super().__init__()
        self.addProperties(UIView.Properties)
