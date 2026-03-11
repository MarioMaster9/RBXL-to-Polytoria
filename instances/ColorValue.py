from .ValueBase import ValueBase
class ColorValue(ValueBase):
    ClassName = "ColorValue"
    Properties = [
        ["Value", "color"]
    ]
    def __init__(self):
        super().__init__()
        self.addProperties(ColorValue.Properties)