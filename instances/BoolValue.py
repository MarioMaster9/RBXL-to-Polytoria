from .ValueBase import ValueBase
class BoolValue(ValueBase):
    ClassName = "BoolValue"
    Properties = [
        ["Value", "boolean"]
    ]
    def __init__(self):
        super().__init__()
        self.addProperties(BoolValue.Properties)