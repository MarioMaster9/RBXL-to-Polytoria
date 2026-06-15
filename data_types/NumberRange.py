class NumberRange:
    def __init__(self, min, max):
        self.min = min
        self.max = max
    def json(self):
        return [self.min, self.max]