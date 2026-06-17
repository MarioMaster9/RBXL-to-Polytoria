from .Instance import Instance
from data_types import Vector2
class UIField(Instance):
    ClassName = "UIField"
    Properties = {
        "PositionOffset": "vector2",
        "PositionRelative": "vector2",
        "Rotation": "float",
        "SizeOffset": "vector2",
        "SizeRelative": "vector2",
        "ClipDescendants": "boolean",
        "PivotPoint": "vector2",
        "Scale": "vector2",
        "Visible": "boolean",
        "MaskMode": "int", # TODO
        "IgnoreMouse": "boolean",
        "ZIndex": "int",
    }
    def __init__(self):
        super().__init__()
        self.addProperties(UIField.Properties)
        self.Rotation = 0
        self.PivotPoint = Vector2(0, 1)
        self.Scale = Vector2(1, 1)
