from .Physical import Physical
from .PolytorianModel import PolytorianModel
from rbxl.data_types import Vector3
class NPC(Physical):
    ClassName = "NPC"
    Properties = [
        ["Velocity", "vector3"],
        ["SeatOffset", "vector3"],
        ["Health", "float"],
        ["MaxHealth", "float"],
        ["JumpPower", "float"],
        ["WalkSpeed", "float"],
        ["UseNametag", "boolean"],
        ["NametagOffset", "vector3"],
        ["NametagVisibleRadius", "float"],
        ["DisplayName", "string"],
        ["JumpSound", "resourceref"],
        ["Character", "ref"],
    ]
    def __init__(self):
        super().__init__()
        self.addProperties(NPC.Properties)
        ptm = PolytorianModel()
        self.Character = PolytorianModel()
        ptm.Name = "Character"
        self.addChild(ptm)
        ptm.LocalPosition = Vector3.ZERO
        ptm.LocalRotation = Vector3.ZERO
        ptm.LocalSize = Vector3.ONE