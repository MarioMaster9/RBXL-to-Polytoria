from .Instance import Instance

class GUI(Instance):
    ClassName = "GUI"
    Properties = [
        ["Visible", "boolean"]
    ]
    def __init__(self):
        super().__init__()
        self.addProperties(GUI.Properties)
        self.Visible = True