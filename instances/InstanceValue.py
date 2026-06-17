from .ValueBase import ValueBase
class InstanceValue(ValueBase):
    ClassName = "InstanceValue"
    Properties = {
        "Value": "ref"
    }
    def __init__(self):
        super().__init__()
        self.addProperties(InstanceValue.Properties)