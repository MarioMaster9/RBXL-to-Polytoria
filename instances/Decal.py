from .Dynamic import Dynamic
class Decal(Dynamic):
    ClassName = "Decal"
    Properties = {
        "Image": "resourceref",
        "Energy": "float",
        "Color": "color",
    }
    def __init__(self):
        super().__init__()
        self.addProperties(Decal.Properties)
        self.Energy = 1