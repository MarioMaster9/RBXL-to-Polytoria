from .Instance import Instance
class BodyRotation(Instance):
    ClassName = "BodyRotation"
    Properties = {
        "TargetRotation": "vector3",
        "Force": "float",
        "AcceptanceAngle": "float",
    }
    def __init__(self):
        super().__init__()
        self.addProperties(BodyRotation.Properties)
        self.AcceptanceAngle = 5.0