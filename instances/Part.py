from .Entity import Entity
class Part(Entity):
    ClassName = "Part"
    Properties = {
        "Shape": "int",
        "Material": "int",
    }
    def __init__(self):
        super().__init__()
        self.addProperties(Part.Properties)