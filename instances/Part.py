from .DynamicInstance import DynamicInstance
from enums.Material import Material
from enums.PhysicsMaterialCombine import PhysicsMaterialCombine


class Part(DynamicInstance):
    ClassName = "Part"
    Properties = [
        ["Color", "color"],
        ["Anchored", "boolean"],
        ["CanCollide", "boolean"],
        ["IsSpawn", "boolean"],
        ["Shape", "int"],
        ["Material", "int"],
        ["Velocity", "vector3"],
        ["Drag", "float"],
        ["AngularDrag", "float"],
        ["Mass", "float"],
        ["UseGravity", "boolean"],
        ["Bounciness", "float"],
        ["Friction", "float"],
        ["FrictionCombine", "int"],
        ["BounceCombine", "int"],
        ["CastShadows", "boolean"],
    ]
    def __init__(self):
        super().__init__()
        self.addProperties(Part.Properties)
        self.Anchored = True
        self.Drag = 0
        self.AngularDrag = 0
        self.Mass = 1
        self.UseGravity = True
        self.FrictionCombine = PhysicsMaterialCombine.Average
        self.BounceCombine = PhysicsMaterialCombine.Average
        self.CastShadows = True