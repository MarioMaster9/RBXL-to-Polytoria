from .Dynamic import Dynamic
class Explosion(Dynamic):
    ClassName = "Explosion"
    Properties = {
        "Radius": "float",
        "Force": "float",
        "AffectAnchored": "boolean",
        "Damage": "float",
        "AffectWelds": "boolean",
    }
    def __init__(self):
        super().__init__()
        self.addProperties(Explosion.Properties)
        self.Radius = 10
        self.Force = 5000
        self.AffectAnchored = False
        self.Damage = 100000
        self.AffectWelds = True