from .DynamicInstance import DynamicInstance
from enums import ImageType
from data_types import Vector2, Color4
class Decal(DynamicInstance):
    ClassName = "Decal"
    Properties = [
        ["ImageID", "string"],
        ["ImageType", "int"],
        ["TextureScale", "vector2"],
        ["TextureOffset", "vector2"],
        ["Color", "color"],
        ["CastShadows", "boolean"],
    ]
    def __init__(self):
        super().__init__()
        self.addProperties(Decal.Properties)
        self.ImageType = ImageType.Asset
        self.TextureScale = Vector2.ONE
        self.TextureOffset = Vector2.ZERO
        self.Color = Color4.WHITE
        self.CastShadows = False