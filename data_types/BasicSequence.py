from typing import TypeVar, Generic, List

T = TypeVar('T')

class BasicSequence(Generic[T]):
    def __init__(self, keypoints: List[T]) -> None:
        self.keypoints: List[T] = keypoints
    def addKeypoint(self, keypoint: T) -> None:
        self.keypoints.append(keypoint)
    def getKeypoint(self, index) -> T:
        return self.keypoints[index]
    def linearSpline(self, x: float):
        assert len(self.keypoints) >= 1

        # Off the beginning
        if len(self.keypoints) == 1 or x < self.getKeypoint(0).time:
            return self.getKeypoint(0).getValue()
        
        for i in range(1, len(self.keypoints)):
            if x < self.getKeypoint(i).time:
                alpha = (self.getKeypoint(i).time - x) / (self.getKeypoint(i).time - self.getKeypoint(i - 1).time)
                return self.getKeypoint(i).getValue() * (1 - alpha) + self.getKeypoint(i - 1).getValue() * alpha
        
        # Off the end
        return self.getKeypoint(len(self.keypoints) - 1).getValue()