from .ValueBase import ValueBase

class StringValue(ValueBase):
    ClassName = "StringValue"
    Properties = [
        ["Value", "string"]
    ]
    def __init__(self):
        super().__init__()
        self.addProperties(StringValue.Properties)