from .ValueBase import ValueBase
class Vector2Value(ValueBase):
    ClassName = "Vector2Value"
    Properties = {
        "Value": "vector2"
    }
    def __init__(self):
        super().__init__()
        self.addProperties(Vector2Value.Properties)