class NumberRange:
    def __init__(self, _min, _max):
        self.min = _min
        self.max = _max
    @staticmethod
    def FromXML(elem):
        values = elem.text.split(' ')
        return NumberRange(float(values[0]), float(values[1]))