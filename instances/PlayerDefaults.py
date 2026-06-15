from .Instance import Instance
from rbxl.data_types import Color4
from enums import PlayerMovementModeEnum
class PlayerDefaults(Instance):
    ClassName = "PlayerDefaults"
    Properties = [
        ["MaxHealth", "float"],
        ["WalkSpeed", "float"],
        ["SprintSpeed", "float"],
        ["JumpPower", "float"],
        ["RespawnTime", "float"],
        ["ChatColor", "color"],
        ["ChatColorsEnabled", "boolean"],
        ["CanMove", "boolean"],
        ["StaminaBurn", "float"],
        ["UseStamina", "boolean"],
        ["Stamina", "float"],
        ["MaxStamina", "float"],
        ["StaminaRegen", "float"],
        ["UseHeadTurning", "boolean"],
        ["UseBubbleChat", "boolean"],
        ["AutoLoadAppearance", "boolean"],
        ["LoadAppearanceTools", "boolean"],
        ["MovementMode", "int"],
    ]
    def __init__(self):
        super().__init__()
        self.addProperties(PlayerDefaults.Properties)
        self.MaxHealth = 100
        self.WalkSpeed = 16
        self.JumpPower = 36
        self.ChatColor = Color4.WHITE
        self.ChatColorsEnabled = True
        self.RespawnTime = 5
        self.CanMove = True
        self.SprintSpeed = 25
        self.Stamina = 0
        self.MaxStamina = 3
        self.UseStamina = True
        self.StaminaRegen = 1.2
        self.StaminaBurn = 1.2
        self.UseHeadTurning = True
        self.UseBubbleChat = True
        self.AutoLoadAppearance = True
        self.LoadAppearanceTools = True
        self.MovementMode = PlayerMovementModeEnum.Default
        self.Name = "PlayerDefaults"