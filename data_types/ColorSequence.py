from .BasicSequence import BasicSequence
from .ColorSequenceKeypoint import ColorSequenceKeypoint
from .Color3 import Color3

class ColorSequence(BasicSequence[ColorSequenceKeypoint]):
    @staticmethod
    def FromXML(elem):
        values = elem.text.split(' ')[:-1]
        seq = ColorSequence([])
        for i in range(0, len(values)//5):
            idx = i * 5
            item = values[idx:idx+5]
            _time = float(item[0])
            color = Color3(float(item[1]), float(item[2]), float(item[3]))
            seq.addKeypoint(ColorSequenceKeypoint(_time, color))
        return seq