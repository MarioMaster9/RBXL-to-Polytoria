from .Instance import Instance
class Script(Instance):
    ClassName = "Script"
    Properties = [
        ["Source", "string"],
        ["IsEnabled", "boolean"],
        ["LinkedScript", "resourceref"]
    ]
    def __init__(self):
        super().__init__()
        self.addProperties(Script.Properties)
        self.Source = ""