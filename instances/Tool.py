from .RigidBody import RigidBody
class Tool(RigidBody):
    ClassName = "Tool"
    Properties = [
        ["Droppable", "boolean"],
        ["IconImage", "ref"],
        ["DropEquipCooldown", "float"],
    ]
    def __init__(self):
        super().__init__()
        self.addProperties(Tool.Properties)