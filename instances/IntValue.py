from .ValueBase import ValueBase

class IntValue(ValueBase):
    ClassName = "IntValue"
    Properties = [
        ["Value", "int"]
    ]
    def __init__(self):
        super().__init__()
        self.addProperties(IntValue.Properties)