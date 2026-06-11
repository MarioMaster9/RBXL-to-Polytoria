from .Dynamic import Dynamic
class Text3D(Dynamic):
    ClassName = "Text3D"
    Properties = [
        ["Text", "string"],
        ["FontSize", "float"],
        ["Color", "color"],
        ["OutlineWidth", "int"],
        ["OutlineColor", "color"],
        ["FaceCamera", "boolean"],
        ["HorizontalAlignment", "int"],
        ["VerticalAlignment", "int"],
        ["FontAsset", "resourceref"],
        ["UseRichText", "boolean"],
        ["Shaded", "boolean"],
    ]
    def __init__(self):
        super().__init__()
        self.addProperties(Text3D.Properties)