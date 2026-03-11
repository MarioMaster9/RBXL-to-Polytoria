from .DynamicInstance import DynamicInstance
from data_types import Color4, Vector3
class NPC(DynamicInstance):
    ClassName = "NPC"
    Properties = [
        ["HeadColor", "color"],
        ["TorsoColor", "color"],
        ["LeftArmColor", "color"],
        ["RightArmColor", "color"],
        ["LeftLegColor", "color"],
        ["RightLegColor", "color"],
        ["Anchored", "boolean"],
        ["Health", "float"],
        ["MaxHealth", "float"],
        ["WalkSpeed", "float"],
        ["JumpPower", "float"],
        ["ShirtID", "int"],
        ["PantsID", "int"],
        ["FaceID", "int"],
        ["Velocity", "vector3"],
    ]
    def __init__(self):
        super().__init__()
        self.addProperties(NPC.Properties)
        self.HeadColor = Color4.WHITE
        self.TorsoColor = Color4.WHITE
        self.LeftArmColor = Color4.WHITE
        self.RightArmColor = Color4.WHITE
        self.LeftLegColor = Color4.WHITE
        self.RightLegColor = Color4.WHITE
        self.Anchored = True
        self.ShirtID = 0
        self.PantsID = 0
        self.FaceID = 0
        self.Velocity = Vector3.ZERO
        self.Size = Vector3.ONE