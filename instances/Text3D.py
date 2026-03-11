from .DynamicInstance import DynamicInstance
class Text3D(DynamicInstance):
    ClassName = "Text3D"
    Properties = [
        ["Text", "string"],
        ["Color", "color"],
        ["FontSize", "float"],
        ["FaceCamera", "boolean"],
        ["HorizontalAlignment", "int"],
        ["VerticalAlignment", "int"],
        ["Font", "int"],
    ]
    def __init__(self):
        super().__init__()
        self.addProperties(Text3D.Properties)