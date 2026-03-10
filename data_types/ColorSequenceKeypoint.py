class ColorSequenceKeypoint:
    def __init__(self, _time, color):
        self.time = _time
        self.color = color
    def getValue(self):
        return self.color