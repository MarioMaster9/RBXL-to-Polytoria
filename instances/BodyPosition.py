from .Instance import Instance
class BodyPosition(Instance):
    ClassName = "BodyPosition"
    Properties = [
        ["TargetPosition", "vector3"],
        ["Force", "float"],
        ["AcceptanceDistance", "float"],
    ]
    def __init__(self):
        super().__init__()
        self.addProperties(BodyPosition.Properties)