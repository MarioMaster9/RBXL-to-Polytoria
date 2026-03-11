from .DynamicInstance import DynamicInstance
from enums import CameraMode
from data_types import Vector3
class Camera(DynamicInstance):
    ClassName = "Camera"
    Properties = [
        ["Mode", "int"],
        ["FOV", "float"],
        ["Orthographic", "boolean"],
        ["OrthographicSize", "float"],
        ["MinDistance", "float"],
        ["MaxDistance", "float"],
        ["ClipThroughWalls", "boolean"],
        ["CanLock", "boolean"],
        ["PositionOffset", "vector3"],
        ["RotationOffset", "vector3"]
    ]
    def __init__(self):
        super().__init__()
        self.addProperties(Camera.Properties)
        self.Mode = CameraMode.FollowPlayer
        self.FOV = 60
        self.Orthographic = False
        self.OrthographicSize = 5
        self.MinDistance = 0
        self.MaxDistance = 150
        self.ClipThroughWalls = False
        self.CanLock = True
        self.PositionOffset = Vector3.ZERO
        self.RotationOffset = Vector3.ZERO
        self.Position = Vector3(0, 8, 0)
        self.Rotation = Vector3.ZERO
        self.Size = Vector3.ONE
        self.Name = "Camera"