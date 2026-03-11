from .Instance import Instance
class PlayerGUI(Instance):
    ClassName = "PlayerGUI"
    Properties = [
        ["Interactable", "boolean"],
        ["Opacity", "float"],
    ]
    def __init__(self):
        super().__init__()
        self.addProperties(PlayerGUI.Properties)
        self.Interactable = True
        self.Opacity = 1
        self.Name = "PlayerGUI"