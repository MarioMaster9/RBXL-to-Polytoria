from .Light import Light
class SpotLight(Light):
    ClassName = "SpotLight"
    Properties = {
        "Range": "float",
        "Angle": "float",
    }
    def __init__(self):
        super().__init__()
        self.addProperties(SpotLight.Properties)
