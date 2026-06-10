from .Instance import Instance
class Clothing(Instance):
    ClassName = "Clothing"
    Properties = [
        ["Image", "ref"]
    ]
    def __init__(self):
        super().__init__()
        self.addProperties(Clothing.Properties)