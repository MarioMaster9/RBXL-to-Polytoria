from .DynamicInstance import DynamicInstance
class Tool(DynamicInstance):
    ClassName = "Tool"
    Properties = [
        ["Droppable", "boolean"],
    ]
    def __init__(self):
        super().__init__()
        self.addProperties(Tool.Properties)