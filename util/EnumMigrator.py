from enums import *
from rbxl.data_types import *

conversionTable = {}

conversionTable[Enum.Material] = {
    Enum.Material.SmoothPlastic: PartMaterialEnum.SmoothPlastic,
    Enum.Material.Wood:          PartMaterialEnum.Wood,
    Enum.Material.Concrete:      PartMaterialEnum.Concrete,
    Enum.Material.Neon:          PartMaterialEnum.Neon,
    Enum.Material.Metal:         PartMaterialEnum.Metal, # Darker
    Enum.Material.Brick:         PartMaterialEnum.Brick,
    Enum.Material.Grass:         PartMaterialEnum.Grass,
    Enum.Material.Ground:        PartMaterialEnum.Dirt,
    Enum.Material.Slate:         PartMaterialEnum.Stone,
    Enum.Material.Snow:          PartMaterialEnum.Snow,
    Enum.Material.Ice:           PartMaterialEnum.Ice,
    Enum.Material.CorrodedMetal: PartMaterialEnum.RustyIron,
    Enum.Material.Sand:          PartMaterialEnum.Sand,
    Enum.Material.Sandstone:     PartMaterialEnum.Sandstone,
    Enum.Material.Plastic:       PartMaterialEnum.Plastic,
#   "?":                         PartMaterialEnum.Plywood,
    Enum.Material.WoodPlanks:    PartMaterialEnum.Planks,
#   "?2":                        PartMaterialEnum.MetalGrid,
    Enum.Material.DiamondPlate:  PartMaterialEnum.MetalPlate,
    Enum.Material.Fabric:        PartMaterialEnum.Fabric,
    Enum.Material.Marble:        PartMaterialEnum.Marble
}

conversionTable[Enum.Style] = {
    Enum.Style.AlternatingSupports: ShapeEnum.Truss,
    Enum.Style.BridgeStyleSupports: ShapeEnum.Truss,
    Enum.Style.NoSupports: ShapeEnum.Frame
}

conversionTable[Enum.TextXAlignment] = {
    Enum.TextXAlignment.Left:   TextHorizontalAlignmentEnum.Left,
    Enum.TextXAlignment.Center: TextHorizontalAlignmentEnum.Center,
    Enum.TextXAlignment.Right:  TextHorizontalAlignmentEnum.Right,
}

conversionTable[Enum.TextYAlignment] = {
    Enum.TextYAlignment.Top:    TextVerticalAlignmentEnum.Top,
    Enum.TextYAlignment.Center: TextVerticalAlignmentEnum.Middle,
    Enum.TextYAlignment.Bottom: TextVerticalAlignmentEnum.Bottom,
}

conversionTable[Enum.FontWeight] = {
    Enum.FontWeight.Thin:        FontWeightEnum.Thin,
    Enum.FontWeight.ExtraLight:  FontWeightEnum.ExtraLight,
    Enum.FontWeight.Light:       FontWeightEnum.Light,
    Enum.FontWeight.Regular:     FontWeightEnum.Regular,
    Enum.FontWeight.Medium:      FontWeightEnum.Medium,
    Enum.FontWeight.SemiBold:    FontWeightEnum.SemiBold,
    Enum.FontWeight.Bold:        FontWeightEnum.Bold,
    Enum.FontWeight.ExtraBold:   FontWeightEnum.ExtraBold,
    Enum.FontWeight.Heavy:       FontWeightEnum.Black,
}

conversionTable[Enum.ResamplerMode] = {
    Enum.ResamplerMode.Default: TextureFilterEnum.Linear,
    Enum.ResamplerMode.Pixelated: TextureFilterEnum.Nearest,
}

class EnumMigrator:
    @staticmethod
    def ToPolytoria(enum, enumValue, defaultValue=0):
        enumConv = conversionTable[enum]
        return enumConv.get(enumValue,defaultValue)