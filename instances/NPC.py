from .Physical import Physical
from .PolytorianModel import PolytorianModel
from .Sound import Sound
from data_types import Vector3
from enums import BuiltInAudioPresetEnum
from .resources.ResourceFactory import ResourceFactory
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
        ["JumpSound", "ref"],
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

        jumpSound = Sound()
        jumpSound.Name = "JumpSound"
        self.addChild(jumpSound)
        jumpSound.Volume = 0.5
        jumpSound.Audio = ResourceFactory.CreateBuiltInAudioAsset(BuiltInAudioPresetEnum.Jump)
        jumpSound.Autoplay = False
        jumpSound.Loop = False
        jumpSound.PlayInWorld = True

        self.JumpSound = jumpSound

        jumpSound.LocalPosition = Vector3.ZERO
        jumpSound.LocalRotation = Vector3.ZERO
        jumpSound.LocalSize = Vector3.ONE

