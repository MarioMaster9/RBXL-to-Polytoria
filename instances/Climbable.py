from .Part import Part

class Climbable(Part):
    ClassName = "Climbable"
    Properties = [
        ["ClimbSpeed", "float"],
    ]
    def __init__(self):
        super().__init__()
        self.addProperties(Climbable.Properties)
        self.ClimbSpeed = 1