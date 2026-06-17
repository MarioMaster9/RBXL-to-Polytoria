from .Instance import Instance
class Players(Instance):
    ClassName = "Players"
    Properties = {
        "PlayerCollisionEnabled": "boolean",
        "UseServerAuthority": "boolean",
    }
    def __init__(self):
        super().__init__()
        self.addProperties(Players.Properties)
        self.PlayerCollisionEnabled = True
        self.UseServerAuthority = True
        self.Name = "Players"