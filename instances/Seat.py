from .Part import Part
class Seat(Part):
    ClassName = "Seat"
    Properties = {
        "CanPlayerSit": "boolean",
        "CanNPCSit": "boolean",
        "SitDirectionLocked": "boolean",
    }
    def __init__(self):
        super().__init__()
        self.addProperties(Seat.Properties)
        self.CanPlayerSit = True
        self.CanNPCSit = True
        self.SitDirectionLocked = True
