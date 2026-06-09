from .CharacterModel import CharacterModel
from rbxl.data_types import Color4
class PolytorianModel(CharacterModel):
    ClassName = "PolytorianModel"
    Properties = [
        ["HeadColor", "color"],
        ["TorsoColor", "color"],
        ["LeftArmColor", "color"],
        ["RightArmColor", "color"],
        ["LeftLegColor", "color"],
        ["RightLegColor", "color"],
        ["FaceImage", "ref"],
        ["BodyMesh", "ref"]
    ]
    def __init__(self):
        super().__init__()
        self.addProperties(PolytorianModel.Properties)
        self.HeadColor = Color4.WHITE
        self.TorsoColor = Color4.WHITE
        self.LeftArmColor = Color4.WHITE
        self.RightArmColor = Color4.WHITE
        self.LeftLegColor = Color4.WHITE
        self.RightLegColor = Color4.WHITE
