class NumberPoint:
    def __init__(self, offset, value):
        self.offset = offset
        self.value = value
    def json(self):
        return {
            "Offset": self.offset,
            "Value": self.value
        }

class NumberSeries:
    def __init__(self):
        self.points = []
    def addPoint(self, offset, value):
        self.points.append(NumberPoint(offset, value))
    def json(self):
        return {
            "Points": [x.json() for x in self.points]
        }