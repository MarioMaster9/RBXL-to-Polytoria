from .ColorSequenceKeypoint import ColorSequenceKeypoint
from .Color3 import Color3

class ColorSequence:
    def __init__(self, keypoints):
        self.keypoints = keypoints
    def addKeypoint(self, keypoint):
        self.keypoints.append(keypoint)
    def getKeypoint(self, idx):
        return self.keypoints[idx]
    def linearSpline(self, x):
        assert len(self.keypoints) >= 1
        
        # Off the beginning
        if len(self.keypoints) == 1 or x < self.getKeypoint(0).time:
            return self.getKeypoint(0).color
        
        for i in range(1, len(self.keypoints)):
            if x < self.getKeypoint(i).time:
                alpha = (self.getKeypoint(i).time - x) / (self.getKeypoint(i).time - self.getKeypoint(i - 1).time)
                return self.getKeypoint(i).color * (1 - alpha) + self.getKeypoint(i - 1).color * alpha
        
        # Off the end
        return self.getKeypoint(len(self.keypoints) - 1).color
        
        
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