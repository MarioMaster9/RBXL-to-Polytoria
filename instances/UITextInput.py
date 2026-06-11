from .UIView import UIView
from enums import TextHorizontalAlignmentEnum
class UITextInput(UIView):
    ClassName = "UITextInput"
    Properties = [
        ["Text", "string"],
        ["TextColor", "color"],
        ["JustifyText", "int"],
        ["FontSize", "float"],
        ["AutoSize", "boolean"],
        ["MaxAutoSize", "float"],
        ["MultiLine", "boolean"],
        ["Placeholder", "string"],
        ["PlaceholderColor", "color"],
        ["ReadOnlyColor", "color"],
        ["ReadOnly", "boolean"],
        ["FontAsset", "ref"],
    ]
    @property
    def HorizontalAlignment(self):
        return self.JustifyText
    @HorizontalAlignment.setter
    def HorizontalAlignment(self, value):
        self.JustifyText = value
    def __init__(self):
        super().__init__()
        self.addProperties(UITextInput.Properties)
        self.JustifyText = TextHorizontalAlignmentEnum.Center
        self.FontSize = 16
        self.MaxAutoSize = 16