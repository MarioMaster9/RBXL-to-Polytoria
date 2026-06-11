from .Instance import Instance
class Weld(Instance):
    ClassName = "Weld"
    Properties = [
        ["Part0", "ref"],
        ["Part1", "ref"],
        ["Enabled", "boolean"],
    ]
    def __init__(self):
        super().__init__()
        self.addProperties(Weld.Properties)