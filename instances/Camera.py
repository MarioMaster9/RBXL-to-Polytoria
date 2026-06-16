from .Dynamic import Dynamic
from enums import CameraModeEnum
from data_types import Vector3

DefaultScrollSensitivity = 15

class Camera(Dynamic):
    ClassName = "Camera"
    Properties = [
        ["Mode", "int"],
        ["FOV", "float"],
        ["ClipThroughWalls", "boolean"],
        ["MinDistance", "float"],
        ["MaxDistance", "float"],
        ["ScrollSensitivity", "float"],
        ["Orthographic", "boolean"],
        ["FollowLerp", "boolean"],
        ["LerpSpeed", "float"],
        ["OrthographicSize", "float"],
        ["Near", "float"],
        ["Far", "float"],
        ["PositionOffset", "vector3"],
        ["RotationOffset", "vector3"],
        ["CanLock", "boolean"],
        ["SensitivityMultiplier", "float"],
        ["ScrollLerpSpeed", "float"],
    ]
    def __init__(self):
        super().__init__()
        self.addProperties(Camera.Properties)
        self.Mode = CameraModeEnum.Follow
        self.FOV = 60
        self.ClipThroughWalls = False
        self.MinDistance = 0
        self.MaxDistance = 20#150
        self.ScrollSensitivity = DefaultScrollSensitivity
        self.Orthographic = False
        self.FollowLerp = False
        self.LerpSpeed = 15
        self.OrthographicSize = 1
        self.Near = 0.05
        self.Far = 4000
        self.PositionOffset = Vector3.ZERO
        self.RotationOffset = Vector3.ZERO
        self.CanLock = True
        self.SensitivityMultiplier = 1
        self.ScrollLerpSpeed = 15

        self.Position = Vector3(0, 8, 0)
        self.Rotation = Vector3.ZERO
        self.Size = Vector3.ONE
        self.Name = "Camera"