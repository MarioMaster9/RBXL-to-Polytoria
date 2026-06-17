from .Instance import Instance
class UIStroke(Instance):
    ClassName = "UIStroke"
    Properties = {
        "Thickness": "uiscale",
        "Color": "color"
    }
    def __init__(self):
        super().__init__()
        self.addProperties(UIStroke.Properties)