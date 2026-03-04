class Font:
    Legacy               = 0    # LegacyArial.json
    Arial                = 1
    ArialBold            = 2
    SourceSans           = 3    # SourceSansPro.json
    SourceSansBold       = 4    # SourceSansPro.json
    SourceSansLight      = 5    # SourceSansPro.json
    SourceSansItalic     = 6    # SourceSansPro.json
    Bodoni               = 7    # AccanthisADFStd.json
    Garamond             = 8    # Guru.json
    Cartoon              = 9    # ComicNeueAngular.json
    Code                 = 10   # Inconsolata.json
    Highway              = 11   # HighwayGothic.json
    SciFi                = 12   # Zekton.json
    Arcade               = 13   # PressStart2P.json
    Fantasy              = 14   # Balthazar.json
    Antique              = 15   # RomanAntique.json
    SourceSansSemibold   = 16   # SourceSansPro.json
    Gotham               = 17
    GothamMedium         = 18
    GothamBold           = 19
    GothamBlack          = 20
    AmaticSC             = 21   # AmaticSC.json
    Bangers              = 22   # Bangers.json
    Creepster            = 23   # Creepster.json
    DenkOne              = 24   # DenkOne.json
    Fondamento           = 25   # Fondamento.json
    FredokaOne           = 26   # FredokaOne.json
    GrenzeGotisch        = 27   # GrenzeGotisch.json
    IndieFlower          = 28   # IndieFlower.json
    JosefinSans          = 29   # JosefinSans.json
    Jura                 = 30   # Jura.json
    Kalam                = 31   # Kalam.json
    LuckiestGuy          = 32   # LuckiestGuy.json
    Merriweather         = 33   # Merriweather.json
    Michroma             = 34   # Michroma.json
    Nunito               = 35   # Nunito.json
    Oswald               = 36   # Oswald.json
    PatrickHand          = 37   # PatrickHand.json
    PermanentMarker      = 38   # PermanentMarker.json
    Roboto               = 39   # Roboto.json
    RobotoCondensed      = 40   # RobotoCondensed.json
    RobotoMono           = 41   # RobotoMono.json
    Sarpanch             = 42   # Sarpanch.json
    SpecialElite         = 43   # SpecialElite.json
    TitilliumWeb         = 44   # TitilliumWeb.json
    Ubuntu               = 45   # Ubuntu.json
    BuilderSans          = 46   # BuilderSans.json
    BuilderSansMedium    = 47   # BuilderSans.json
    BuilderSansBold      = 48   # BuilderSans.json
    BuilderSansExtraBold = 49   # BuilderSans.json
    Arimo                = 50   # Arimo.json
    ArimoBold            = 51   # Arimo.json
    Unknown              = 100

class FontSize:
    Size8  = 0
    Size9  = 1
    Size10 = 2
    Size11 = 3
    Size12 = 4
    Size14 = 5
    Size18 = 6
    Size24 = 7
    Size36 = 8
    Size48 = 9
    Size28 = 10
    Size32 = 11
    Size42 = 12
    Size60 = 13
    Size96 = 14

class FontWeight:
    Thin       = 100
    ExtraLight = 200
    Light      = 300
    Regular    = 400
    Medium     = 500
    SemiBold   = 600
    Bold       = 700
    ExtraBold  = 800
    Heavy      = 900

class Material:
    Plastic       = 0x100
    SmoothPlastic = 0x110
    Neon          = 0x120
    Wood          = 0x200
    WoodPlanks    = 0x210
    Marble        = 0x310
    Slate         = 0x320
    Concrete      = 0x330
    Granite       = 0x340
    Brick         = 0x350
    Pebble        = 0x360
    Cobblestone   = 0x370
    Rock          = 0x380
    Sandstone     = 0x390
    Basalt        = 0x314
    CrackedLava   = 0x324
    Limestone     = 0x334
    Pavement      = 0x344
    CorrodedMetal = 0x410
    DiamondPlate  = 0x420
    Foil          = 0x430
    Metal         = 0x440
    Grass         = 0x500
    LeafyGrass    = 0x504
    Sand          = 0x510
    Fabric        = 0x520
    Snow          = 0x530
    Mud           = 0x540
    Ground        = 0x550
    Asphalt       = 0x560
    Salt          = 0x570
    Ice           = 0x600
    Glacier       = 0x610
    Glass         = 0x620
    ForceField    = 0x630
    Air           = 0x700
    Water         = 0x800
    Cardboard     = 0x900
    Carpet        = 0x901
    CeramicTiles  = 0x902
    ClayRoofTiles = 0x903
    RoofShingles  = 0x904
    Leather       = 0x905
    Plaster       = 0x906
    Rubber        = 0x907

class MeshType:
    Head           = 0
    Torso          = 1
    Wedge          = 2
    Sphere         = 3
    Cylinder       = 4
    FileMesh       = 5
    Brick          = 6
    Prism          = 7
    Pyramid        = 8
    ParallelRamp   = 9
    RightAngleRamp = 10
    CornerWedge    = 11

class NormalId:
    Right  = 0
    Top    = 1
    Back   = 2
    Left   = 3
    Bottom = 4
    Front  = 5

class PartType:
    Ball        = 0
    Block       = 1
    Cylinder    = 2
    Wedge       = 3
    CornerWedge = 4

class TextXAlignment:
    Left   = 0
    Right  = 1
    Center = 2

class TextYAlignment:
    Top    = 0
    Center = 1
    Bottom = 2
