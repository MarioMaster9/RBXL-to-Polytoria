from .Part import Part
class Truss(Part):
    ClassName = "Truss"
    Properties = [
        ["ClimbSpeed", "float"],
    ]
    def __init__(self):
        super().__init__()
        self.addProperties(Truss.Properties)
        self.ClimbSpeed = 1