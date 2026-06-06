from .Dynamic import Dynamic
from rbxl.data_types import Vector2, Color4
class Image3D(Dynamic):
    ClassName = "Image3D"
    Properties = [
        ["Image", "ref"],
        ["TextureScale", "vector2"],
        ["TextureOffset", "vector2"],
        ["Color", "color"],
        ["CastShadows", "boolean"],
    ]
    def __init__(self):
        super().__init__()
        self.addProperties(Image3D.Properties)
        self.TextureScale = Vector2.ONE
        self.TextureOffset = Vector2.ZERO
        self.Color = Color4.WHITE
        self.CastShadows = False