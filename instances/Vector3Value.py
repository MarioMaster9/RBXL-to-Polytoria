from .ValueBase import ValueBase
class Vector3Value(ValueBase):
    ClassName = "Vector3Value"
    Properties = [
        ["Value", "vector3"]
    ]
    def __init__(self):
        super().__init__()
        self.addProperties(Vector3Value.Properties)