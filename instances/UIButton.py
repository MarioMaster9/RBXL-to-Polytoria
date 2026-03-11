from .UILabel import UILabel
class UIButton(UILabel):
    ClassName = "UIButton"
    Properties = [
        ["Interactable", "boolean"],
    ]
    def __init__(self):
        super().__init__()
        self.addProperties(UIButton.Properties)
