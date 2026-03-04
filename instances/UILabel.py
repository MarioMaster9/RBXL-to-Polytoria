from .UIView import UIView
from enums.TextJustify import TextJustify
from enums.TextFontPreset import TextFontPreset

class UILabel(UIView):
    ClassName = "UILabel"
    Properties = [
        ["Text", "string"],
        ["TextColor", "color"],
        ["JustifyText", "int"],
        ["VerticalAlign", "int"],
        ["FontSize", "float"],
        ["MaxFontSize", "float"],
        ["AutoSize", "boolean"],
        ["Font", "int"],
        ["OutlineColor", "color"],
        ["OutlineWidth", "float"],
    ]
    def __init__(self):
        super().__init__()
        self.addProperties(UILabel.Properties)
        self.JustifyText = TextJustify.Center
        self.FontSize = 16
        self.MaxFontSize = 16
        self.Font = TextFontPreset.SourceSans
        self.OutlineWidth = 0.2