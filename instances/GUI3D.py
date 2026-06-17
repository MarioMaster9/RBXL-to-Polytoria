from .Dynamic import Dynamic
class GUI3D(Dynamic):
    ClassName = "GUI3D"
    Properties = {
        "Shaded": "boolean",
        "FaceCamera": "boolean",
        "Transparent": "boolean",
    }
    def __init__(self):
        super().__init__()
        self.addProperties(GUI3D.Properties)
        self.Shaded = False
        self.FaceCamera = False
        self.Transparent = True