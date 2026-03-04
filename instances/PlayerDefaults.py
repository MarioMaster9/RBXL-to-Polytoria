from .Instance import Instance
from data_types.Color4 import Color4

class PlayerDefaults(Instance):
    ClassName = "PlayerDefaults"
    Properties = [
        ["MaxHealth", "float"],
        ["WalkSpeed", "float"],
        ["SprintSpeed", "float"],
        ["StaminaEnabled", "boolean"],
        ["Stamina", "float"],
        ["MaxStamina", "float"],
        ["StaminaRegen", "float"],
        ["JumpPower", "float"],
        ["RespawnTime", "float"],
        ["ChatColor", "color"],
    ]
    def __init__(self):
        super().__init__()
        self.addProperties(PlayerDefaults.Properties)
        self.MaxHealth = 100
        self.WalkSpeed = 16
        self.SprintSpeed = 25
        self.StaminaEnabled = True
        self.Stamina = 0
        self.MaxStamina = 3
        self.StaminaRegen = 1.2
        self.JumpPower = 36
        self.RespawnTime = 5
        self.ChatColor = Color4.WHITE
        self.Name = "PlayerDefaults"