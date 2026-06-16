from .Dynamic import Dynamic
from data_types import Vector2, Color
from enums import TextureFilterEnum
class Image3D(Dynamic):
    ClassName = "Image3D"
    Properties = [
        ["Image", "resourceref"],
        ["TextureScale", "vector2"],
        ["TextureOffset", "vector2"],
        ["Color", "color"],
        ["CastShadows", "boolean"],
        ["Shaded", "boolean"],
        ["FaceCamera", "boolean"],
        ["DoubleSided", "boolean"],
        ["TextureFilter", "int"],
    ]
    def __init__(self):
        super().__init__()
        self.addProperties(Image3D.Properties)
        self.TextureScale = Vector2.ONE
        self.TextureOffset = Vector2.ZERO
        self.Color = Color(1, 1, 1)
        self.CastShadows = False
        self.Shaded = True
        self.FaceCamera = False
        self.DoubleSided = False
        self.TextureFilter = TextureFilterEnum.Linear