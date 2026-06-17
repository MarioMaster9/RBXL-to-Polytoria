from .CharacterModel import CharacterModel
from data_types import Color
class PolytorianModel(CharacterModel):
    ClassName = "PolytorianModel"
    Properties = {
        "HeadColor": "color",
        "TorsoColor": "color",
        "LeftArmColor": "color",
        "RightArmColor": "color",
        "LeftLegColor": "color",
        "RightLegColor": "color",
        "FaceImage": "resourceref",
        "BodyMesh": "resourceref"
    }
    def __init__(self):
        super().__init__()
        self.addProperties(PolytorianModel.Properties)
        self.HeadColor = Color(1, 1, 1)
        self.TorsoColor = Color(1, 1, 1)
        self.LeftArmColor = Color(1, 1, 1)
        self.RightArmColor = Color(1, 1, 1)
        self.LeftLegColor = Color(1, 1, 1)
        self.RightLegColor = Color(1, 1, 1)
