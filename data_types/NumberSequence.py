from .NumberSequenceKeypoint import NumberSequenceKeypoint
from .Color3 import Color3

class NumberSequence:
    def __init__(self):
        self.keypoints = []
    def addKeypoint(self, keypoint):
        self.keypoints.append(keypoint)
    @staticmethod
    def FromXML(elem):
        values = elem.text.split(' ')[:-1]
        seq = NumberSequence()
        for i in range(0, len(values)//3):
            idx = i * 3
            item = values[idx:idx+3]
            _time = float(item[0])
            number = float(item[1])
            seq.addKeypoint(NumberSequenceKeypoint(_time, number))
        return seq