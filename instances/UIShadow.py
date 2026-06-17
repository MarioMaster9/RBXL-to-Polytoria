from .Instance import Instance
class UIShadow(Instance):
    ClassName = "UIShadow"
    Properties = {
        "Layers": "array",
    }
    def __init__(self):
        super().__init__()
        self.addProperties(UIShadow.Properties)