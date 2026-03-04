from .Instance import Instance

class Players(Instance):
    ClassName = "Players"
    Properties = [
        ["PlayerCollisionEnabled", "boolean"]
    ]
    def __init__(self):
        super().__init__()
        self.addProperties(Players.Properties)
        self.PlayerCollisionEnabled = True
        self.Name = "Players"