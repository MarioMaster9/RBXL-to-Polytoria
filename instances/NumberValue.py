from .ValueBase import ValueBase

class NumberValue(ValueBase):
    ClassName = "NumberValue"
    Properties = [
        ["Value", "float"]
    ]
    def __init__(self):
        super().__init__()
        self.addProperties(NumberValue.Properties)