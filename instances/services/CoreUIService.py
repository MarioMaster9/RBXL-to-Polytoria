from ..Instance import Instance
class CoreUIService(Instance):
    ClassName = "CoreUIService"
    Properties = [
        ["UseUserCard", "boolean"],
        ["UseChat", "boolean"],
        ["UseHealthBar", "boolean"],
        ["UseLeaderboard", "boolean"],
        ["UseHotbar", "boolean"],
        ["UseBackpack", "boolean"],
        ["UseMenuButton", "boolean"],
        ["UseEmoteWheel", "boolean"],
        ["CanRespawn", "boolean"],
    ]
    def __init__(self):
        super().__init__()
        self.addProperties(CoreUIService.Properties)
        self.Name = "CoreUI"
        self.UseUserCard = True
        self.UseChat = True
        self.UseHealthBar = True
        self.UseLeaderboard = True
        self.UseHotbar = True
        self.UseBackpack = True
        self.UseMenuButton = True
        self.UseEmoteWheel = True
        self.CanRespawn = True
        