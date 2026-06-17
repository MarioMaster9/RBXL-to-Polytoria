from .Light import Light
class PointLight(Light):
    ClassName = "PointLight"
    Properties = {
        "Range": "float",
    }
    def __init__(self):
        super().__init__()
        self.addProperties(PointLight.Properties)