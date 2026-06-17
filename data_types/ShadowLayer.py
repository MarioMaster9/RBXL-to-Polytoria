class ShadowLayer:
    def __init__(self, color, offset, radius, spread, blendMode):
        self.color = color
        self.offset = offset
        self.radius = radius
        self.spread = spread
        self.blendMode = blendMode
    def json(self):
        return {
            "Color": self.color.json(),
            "Offset": self.offset.json(),
            "Radius": self.radius,
            "Spread": self.spread,
            "BlendMode": self.blendMode
        }