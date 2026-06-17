class ColorPoint:
    def __init__(self, offset, color):
        self.offset = offset
        self.color = color
    def json(self):
        return {
            "Offset": self.offset,
            "Color": self.color.json()
        }

class ColorSeries:
    def __init__(self):
        self.points = []
    def addPoint(self, offset, color):
        self.points.append(ColorPoint(offset, color))
    def json(self):
        return {
            "Points": [x.json() for x in self.points]
        }