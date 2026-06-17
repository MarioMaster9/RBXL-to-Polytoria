from .UIView import UIView
from enums import TextHorizontalAlignmentEnum, TextVerticalAlignmentEnum
class UILabel(UIView):
    ClassName = "UILabel"
    Properties = {
        "Text": "string",
        "TextColor": "color",
        "OutlineWidth": "float",
        "OutlineColor": "color",
        "HorizontalAlignment": "int",
        "VerticalAlignment": "int",
        "FontSize": "float",
        "AutoSize": "boolean",
        "MaxAutoSize": "float",
        "UseRichText": "boolean",
        "FontAsset": "resourceref",
        "TextTrimming": "int",
        "TextWrapped": "boolean",
    }
    def __init__(self):
        super().__init__()
        self.addProperties(UILabel.Properties)
        self.HorizontalAlignment = TextHorizontalAlignmentEnum.Center
        self.VerticalAlignment = TextVerticalAlignmentEnum.Middle
        self.FontSize = 16
        self.MaxAutoSize = 16
        self.OutlineWidth = 0.2