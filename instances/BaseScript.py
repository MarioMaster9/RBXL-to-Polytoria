from .Instance import Instance

class BaseScript(Instance):
    ClassName = "BaseScript"
    Properties = [
        ["Source", "string"],
    ]
    def __init__(self):
        super().__init__()
        self.addProperties(BaseScript.Properties)
        self.Source = ""