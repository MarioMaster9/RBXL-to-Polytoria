from .Instance import Instance
from rbxl.data_types import Vector2
class UIField(Instance):
    ClassName = "UIField"
    Properties = [
        ["PositionOffset", "vector2"],
        ["PositionRelative", "vector2"],
        ["Rotation", "float"],
        ["SizeOffset", "vector2"],
        ["SizeRelative", "vector2"],
        ["PivotPoint", "vector2"],
        ["Visible", "boolean"],
        ["ClipDescendants", "boolean"],
    ]
    def __init__(self):
        super().__init__()
        self.addProperties(UIField.Properties)
        self.Rotation = 0
        self.PivotPoint = Vector2(0, 1)