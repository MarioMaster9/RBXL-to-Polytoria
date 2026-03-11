from .UIView import UIView
from enums import TextJustify, TextFontPreset
class UITextInput(UIView):
    ClassName = "UITextInput"
    Properties = [
        ["Text", "string"],
        ["TextColor", "color"],
        ["JustifyText", "int"],
        ["VerticalAlign", "int"],
        ["FontSize", "float"],
        ["MaxFontSize", "float"],
        ["AutoSize", "boolean"],
        ["Font", "int"],
        ["Placeholder", "string"],
        ["PlaceholderColor", "color"],
        ["IsMultiline", "boolean"],
        ["IsReadOnly", "boolean"],
    ]
    def __init__(self):
        super().__init__()
        self.addProperties(UITextInput.Properties)
        self.JustifyText = TextJustify.Center
        self.FontSize = 16
        self.MaxFontSize = 16
        self.Font = TextFontPreset.SourceSans