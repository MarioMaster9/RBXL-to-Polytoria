class UIScale:
    def __init__(self, offset, scale):
        self.offset = offset
        self.scale = scale
    def json(self):
        return {
            "Offset": self.offset,
            "Scale": self.scale,
        }