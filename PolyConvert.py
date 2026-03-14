from multimethod import multimethod
import json
import rbxl
from json.decoder import JSONDecodeError

import shutil
import math
import util.hashfuncs as hashfuncs
import argparse
import os

from rbxl.data_types import *
from enums import *
from instances import *

import util.extmath as extmath

from util.LightingParameters     import LightingParameters
from util.BufferedXMLWriter      import BufferedXMLWriter
from rbxl.util.InstanceTree      import TreeItem

def removeFolder(folder):
    try:
        shutil.rmtree(folder)
    except FileNotFoundError:
        pass

def remakeFolder(folder):
    removeFolder(folder)
    os.mkdir(folder)

parser = argparse.ArgumentParser(
                    prog='RBXL to Polytoria',
                    description='Converts RBXL files to Polytoria (XML format only)')
parser.add_argument('filename')
parser.add_argument('-o', '--outfile', default='final', help='File to output (without extension)')
parser.add_argument('-n', '--npcs', action='store_true', help='Specify whether to convert NPCs or not')
parser.add_argument('-c', '--config', help='Configuration file (see: config-template.json)')

config_assets = {
    "rbxasset://fonts/sword.mesh": "130473"
}
config_scriptNames = {}

args = parser.parse_args()

if not args.config is None:
    try:
        with open(args.config, 'r') as f:
            data = json.load(f)
            config_assets.update(data['assets'])
            config_scriptNames = data['scriptNames']
    except FileNotFoundError:
        print(f'Configuration file {args.config} not found! Proceeding without configuration')
    except JSONDecodeError:
        print(f'Configuration file {args.config} malformed! Proceeding without configuration')

remakeFolder('scripts')
remakeFolder('embedded')
remakeFolder('out')

game = Game("1.5.2")

services = {}

root = rbxl.parse(args.filename)
for child in root.children:
    services[child.className] = child
writer = BufferedXMLWriter(f'out/{args.outfile}.poly')

mirrorMul = Vector3(-1, 1, 1)

def mirrorVector(v):
    # positions are mirrored
    return v * mirrorMul

# convert transparency to opacity
def alpha(transparency):
    return 1-min(1, transparency)

def getPartColor(obj):
    return obj.get('Color3uint8', BrickColor.ColorMap[obj.get('BrickColor')])

def getPhysicalProperties(obj):
    # legacyPhysicalProperties is here so that i don't have to have extra code to handle legacy physics properties separately
    legacyPhysicalProperties = {
        "Friction": obj.get('Friction'),
        "Elasticity": obj.get('Elasticity'),
        "Density": 1,
        "FrictionWeight": 1,
        "ElasticityWeight": 1,
        "AcousticAbsorption": 1
    }
    return obj.get('CustomPhysicalProperties', legacyPhysicalProperties)

def getPartFriction(obj):
    return getPhysicalProperties(obj).get('Friction')

def getPartElasticity(obj):
    return getPhysicalProperties(obj).get('Elasticity')

@multimethod
def getColor4(obj: TreeItem, propType: str):
    # color4 method, assuming that the format will always be propType followed by "Color3" for color, or propType followed by "Transparency" for transparency
    # Mainly used for GUI objects
    return Color4.FromColor3(obj.get(propType + "Color3", Color3.BLACK), alpha(obj.get(propType + "Transparency", 1)))

@multimethod
def getColor4(obj: TreeItem, color3: str, transparency: str):
    # color4 method, separating property names. safer, but it may look messier
    return Color4.FromColor3(obj.get(color3), alpha(obj.get(transparency)))

def getPartColor4(obj):
    # color4 method for parts, due to part color property name and datatype changes in various versions
    return Color4.FromColor3(getPartColor(obj), alpha(obj.get('Transparency')))

materialLookup = {
    Enum.Material.SmoothPlastic: Material.SmoothPlastic,
    Enum.Material.Wood:          Material.Wood,
    Enum.Material.Concrete:      Material.Concrete,
    Enum.Material.Neon:          Material.Neon,
    Enum.Material.Metal:         Material.Metal, # Darker
    Enum.Material.Brick:         Material.Brick,
    Enum.Material.Grass:         Material.Grass,
    Enum.Material.Ground:        Material.Dirt,
    Enum.Material.Slate:         Material.Stone,
    Enum.Material.Snow:          Material.Snow,
    Enum.Material.Ice:           Material.Ice,
    Enum.Material.CorrodedMetal: Material.RustyIron,
    Enum.Material.Sand:          Material.Sand,
    Enum.Material.Sandstone:     Material.Sandstone,
    Enum.Material.Plastic:       Material.Plastic,
#   "?":                         Material.Plywood,
    Enum.Material.WoodPlanks:    Material.Planks,
#   "?2":                        Material.MetalGrid,
    Enum.Material.DiamondPlate:  Material.MetalPlate,
    Enum.Material.Fabric:        Material.Fabric,
    Enum.Material.Marble:        Material.Marble
}

# list containing missing assets, used so that the console isn't flooded by duplicates
missingAssets = []

def getResource(res):
    if type(res) is str:
        # bad code
        res = Content(res)
    if res.identifier in missingAssets:
        return "0"
    resId = "0"
    if res.identifier == "":
        return resId
    if res.identifier in config_assets:
        resId = config_assets[res.identifier]
    else:
        print("MISSING ASSET: " + res.identifier)
        missingAssets.append(res.identifier)
    return resId

# None is defined here so that i don't have to have an extra if statement for getting the replacement script source
scriptSources = {
    None: ""
}

for _, name in config_scriptNames.items():
    with open(f"replacements/{name}.lua", "r") as f:
        scriptSources[name] = f.read()

def saveScript(source, sourceHash):
    with open(f'scripts/{sourceHash}.lua', 'wb+') as f:
        f.write(source.encode('utf-8'))

def getScriptSource(scriptHash):
    return scriptSources[config_scriptNames.get(scriptHash)]

def isValidCharacter(mdl):
    if mdl.className != 'Model':
        return False
    if not mdl.getcustom('hasHumanoid'):
        return False
    if mdl.findFirstChild("Torso") is None:
        return False
    if mdl.findFirstChild("Head") is None:
        return False
    return True

def fixRotation(rot):
    rot.orthonormalize() # Orthonormalize the rotation so that getting euler angles doesn't result in weird values
    euler = extmath.degrees(Vector3(*rot.toEulerAnglesYXZ()).yxz())
    euler.y = -euler.y
    euler.z = -euler.z
    return euler

def getRotationAndPosition(cf):
    return fixRotation(cf.rotation), mirrorVector(cf.translation)

def HandleModel(obj, polyObject):
    pass

def HandleNPC(obj, polyObject):
    shirt = obj.findFirstChildOfClass("Shirt")
    if not shirt is None:
        polyObject.ShirtID = int(getResource(shirt.get('ShirtTemplate')))
    pants = obj.findFirstChildOfClass("Pants")
    if not pants is None:
        polyObject.PantsID = int(getResource(pants.get('PantsTemplate')))
    humanoid = obj.findFirstChildOfClass("Humanoid")
    head = obj.findFirstChild("Head")
    if not head is None:
        polyObject.HeadColor = getPartColor4(head)
    torso = obj.findFirstChild("Torso")
    if not torso is None:
        polyObject.TorsoColor = getPartColor4(torso)
    leftArm = obj.findFirstChild("Left Arm")
    if not leftArm is None:
        polyObject.LeftArmColor = getPartColor4(leftArm)
    rightArm = obj.findFirstChild("Right Arm")
    if not rightArm is None:
        polyObject.RightArmColor = getPartColor4(rightArm)
    leftLeg = obj.findFirstChild("Left Leg")
    if not leftLeg is None:
        polyObject.LeftLegColor = getPartColor4(leftLeg)
    rightLeg = obj.findFirstChild("Right Leg")
    if not rightLeg is None:
        polyObject.RightLegColor = getPartColor4(rightLeg)
    bodyColors = obj.findFirstChildOfClass("BodyColors")
    if not bodyColors is None:
        polyObject.HeadColor.setColor3(bodyColors.get('HeadColor'))
        polyObject.TorsoColor.setColor3(bodyColors.get('TorsoColor'))
        polyObject.LeftArmColor.setColor3(bodyColors.get('LeftArmColor'))
        polyObject.RightArmColor.setColor3(bodyColors.get('RightArmColor'))
        polyObject.LeftLegColor.setColor3(bodyColors.get('LeftLegColor'))
        polyObject.RightLegColor.setColor3(bodyColors.get('RightLegColor'))
    
    polyObject.Health = humanoid.get('Health_XML', humanoid.get('Health'))
    polyObject.MaxHealth = humanoid.get('MaxHealth')
    polyObject.WalkSpeed = humanoid.get('WalkSpeed')
    polyObject.JumpPower = humanoid.get('JumpPower', 30)
    rotation, position = getRotationAndPosition(torso.get('CFrame'))
    rotation.y = (rotation.y + 180) % 360
    polyObject.Position = position
    polyObject.Rotation = rotation

def HandleValue(obj, polyObject):
    polyObject.Value = obj.get('Value')

def HandleColorValue(obj, polyObject):
    polyObject.Value = Color4.FromColor3(obj.get('Value'))

cylinderEuler    = Vector3(  0, 0, 90) # Regular cylinders in polytoria face up
wedgeEuler       = Vector3( 90, 0,  0) # Wedges are mirrored i think
cornerWedgeEuler = Vector3(-90, 0,  0)

cylinderTransform    = Matrix3.fromEulerAnglesYXZ(*extmath.radians(cylinderEuler))
wedgeTransform       = Matrix3.fromEulerAnglesYXZ(*extmath.radians(wedgeEuler))
cornerWedgeTransform = Matrix3.fromEulerAnglesYXZ(*extmath.radians(cornerWedgeEuler))

typeTransforms = {
    "Wedge":       wedgeTransform,
    "Cylinder":    cylinderTransform,
    "CornerWedge": cornerWedgeTransform
}

meshClasses = [
    'SpecialMesh',
    'CylinderMesh',
    'BlockMesh',
    'FileMesh'
]

meshPhysicalShapes = {
    Enum.MeshType.Head:     "UpCylinder",
    Enum.MeshType.Torso:    "Block",
    Enum.MeshType.Wedge:    "Wedge",
    Enum.MeshType.Sphere:   "SphereMesh",
    Enum.MeshType.Cylinder: "Cylinder",
    Enum.MeshType.FileMesh: "FileMesh",
    Enum.MeshType.Brick:    "Block"
}

partPhysicalShapes = {
    Enum.PartType.Ball:        "Ball",
    Enum.PartType.Block:       "Block",
    Enum.PartType.Cylinder:    "Cylinder",
    Enum.PartType.Wedge:       "Wedge",
    Enum.PartType.CornerWedge: "CornerWedge"
}

classPhysicalShapes = {
    "UnionOperation":  "FileMesh",
    "WedgePart":       "Wedge",
    "CornerWedgePart": "CornerWedge",
    "TrussPart":       "Truss"
}

def getAppliedMeshInfo(obj):
    shape = None
    uri = Content.EMPTY
    textureUri = Content.EMPTY
    if obj.className == "MeshPart":
        return MeshInfo('FileMesh', obj.get('MeshId'), textureUri, Vector3.ZERO, obj.get('size'), Vector3.ONE)
    for child in reversed(obj.children):
        if not child.className in meshClasses:
            continue
        offset = child.get('Offset', Vector3.ZERO)
        scale = child.get('Scale', Vector3.ONE)
        vertexColor = child.get('VertexColor', Vector3.ONE)
        className = child.className
        if className == 'SpecialMesh':
            meshType = child.get('MeshType')
            if meshType == Enum.MeshType.FileMesh:
                className = 'FileMesh'
        match className:
            case 'SpecialMesh':
                meshType = child.get('MeshType')
                if not meshType in meshPhysicalShapes:
                    return MeshInfo.EMPTY
                shape = meshPhysicalShapes.get(meshType)
                scale *= obj.get('size')
            case 'FileMesh':
                uri = child.get('MeshId')
                textureUri = child.get('TextureId')
                shape = 'FileMesh'
            case 'CylinderMesh':
                shape = 'UpCylinder'
                scale *= obj.get('size')
            case 'BlockMesh':
                shape = 'Block'
                scale *= obj.get('size')
        return MeshInfo(shape, uri, textureUri, offset, scale, vertexColor)
    if obj.className == "UnionOperation":
        uri = obj.get('AssetId')
    if obj.className in classPhysicalShapes:
        shape = classPhysicalShapes[obj.className]
    else:
        shape = partPhysicalShapes[obj.get('shape', Enum.PartType.Block)]
    return MeshInfo(shape, uri, textureUri, Vector3.ZERO, obj.get('size'), Vector3.ONE)

# Instances derived from part that have additional functionality
functionalParts = [
    'TrussPart',
    'Seat',
    'VehicleSeat'
]

def PartModifier(obj):
    classname = "Part"
    if obj.className in functionalParts:
        classname = obj.className
    mesh = getAppliedMeshInfo(obj)
    obj.setcustom('meshInfo', mesh)
    if not mesh.exists:
        return classname
    if mesh.type != "FileMesh":
        return classname
    if mesh.id.identifier in meshIdMap:
        return classname
    obj.set("MeshId", mesh.id)
    return "MeshPart"

meshIdMap = {
    "1033714": {"shape": PartShape.Cone, "scale": Vector3(2, 0.75, 2)}
}

typeShapes = {
    "UpCylinder": PartShape.Cylinder,
    "Cylinder": PartShape.Cylinder,
    "Block": PartShape.Brick,
    "SphereMesh": PartShape.Ball,
    "Ball": PartShape.Ball,
    "Wedge": PartShape.Wedge,
    "CornerWedge": PartShape.CornerWedge,
    "FileMesh": PartShape.Brick
}

trussShapes = {
    Enum.Style.AlternatingSupports: PartShape.Truss,
    Enum.Style.BridgeStyleSupports: PartShape.Truss,
    Enum.Style.NoSupports: PartShape.TrussFrame
}

def getExtraPartInfo(obj):
    meshInfo = obj.getcustom('meshInfo')
    if meshInfo.type == 'FileMesh':
        if meshInfo.id.identifier in meshIdMap:
            info = meshIdMap[meshInfo.id.identifier]
            return info['shape'], info['scale']
    elif meshInfo.type == 'Truss':
        trussStyle = obj.get('style')
        return trussShapes[trussStyle], Vector3.ONE
    return typeShapes.get(meshInfo.type, PartShape.Brick), Vector3.ONE

def HandlePart(obj, polyObject):
    size = Vector3.ONE
    shape, scale = getExtraPartInfo(obj)

    meshInfo = obj.getcustom('meshInfo')
    
    size = meshInfo.scale * scale
    vertexColor = meshInfo.vertexColor

    # use the transform defined for the specified type. otherwise, use the identity matrix
    transform = typeTransforms.get(meshInfo.type, Matrix3.IDENTITY)
    decalSize = size
    match meshInfo.type:
        case 'Cylinder' | 'UpCylinder':
            if meshInfo.type == "Cylinder":
                # Regular cylinder shape is on it's side, so modify size to be equivalent to UpCylinder
                decalSize = decalSize.yxz()
            # modify size to be the smallest of the horizontal sizes, matching the behavior in roblox
            minSize = min(decalSize.x, decalSize.z)
            decalSize = Vector3(minSize, decalSize.y, minSize)
            size = decalSize.copy() # store a copy of the modified size so that the code afterwards doesn't affect the copy
            if meshInfo.type == "Cylinder":
                # Restore the size
                decalSize = decalSize.yxz()
    obj.setcustom('decalSize', decalSize)
    match meshInfo.type:
        case 'Wedge' | 'CornerWedge':
            size = size.zyx()
    
    # store worldTransform, used by decals to correctly position the faces
    untransformed = CoordinateFrame(Matrix3.IDENTITY, meshInfo.offset)
    transformed = CoordinateFrame(transform, meshInfo.offset)
    obj.setcustom('worldTransform', obj.get('CFrame') * untransformed)
    rotation, position = getRotationAndPosition(obj.get('CFrame') * transformed)
    match obj.className:
        case 'Seat' | 'VehicleSeat':
            # rotate seats so the player doesn't sit in them backwards
            rotation.y = (rotation.y + 180) % 360
    vertexColor.clamp(-Vector3.ONE, Vector3.ONE) # clamp vertexColor so that colors don't end up weird
    partColor = getPartColor4(obj)
    if str(meshInfo.textureId) != '':
        partColor = Color4.FromColor3(Color3(*vertexColor), partColor.a)
    polyObject.Color = partColor
    
    # commented out due to objects not being welded together
    #polyObject.Anchored = obj.get('Anchored')
    polyObject.CanCollide = obj.get('CanCollide')
    polyObject.IsSpawn = obj.className == 'SpawnLocation'
    if polyObject.className != 'MeshPart':
        # MeshPart class doesn't have Shape property afaik
        polyObject.Shape = shape
    
    polyObject.Material = materialLookup.get(obj.get('Material'), Material.Plastic)
    polyObject.Velocity = mirrorVector(obj.get('Velocity'))
    polyObject.Friction = getPartFriction(obj)
    polyObject.Bounciness = getPartElasticity(obj)
        
    polyObject.Position = position
    polyObject.Rotation = rotation
    polyObject.Size = size

def HandleScript(obj, polyObject):
    source = obj.get('Source')
    sourceHash = hashfuncs.md5(source)
    saveScript(source, sourceHash)
    polyObject.Source = getScriptSource(sourceHash)

decalDist = 0.0015
decalOffset = 0.5

# make code look cleaner
pi = math.pi
faceRotations = {
    Enum.NormalId.Right:   Vector3(0,      pi*1.5, 0),
    Enum.NormalId.Top:     Vector3(pi*0.5, 0,      0),
    Enum.NormalId.Back:    Vector3(0,      pi,     0),
    Enum.NormalId.Left:    Vector3(0,      pi*0.5, 0),
    Enum.NormalId.Bottom:  Vector3(pi*1.5, pi,     0),
    Enum.NormalId.Front:   Vector3(0,      0,      0),
}

def HandleDecal(obj, polyObject):
    if str(obj.get('Texture')) == '':
        polyObject.Color = Color4(0, 0, 0, 0)
    polyObject.ImageID = getResource(obj.get('Texture'))
    if not isinstance(polyObject.parent, Part):
        polyObject.Size = Vector3.ZERO
        return
    size = obj.parent.getcustom('decalSize')
    face = obj.get('Face')
    worldTransform = obj.parent.getcustom('worldTransform')
    faceNormal = Vector3.FromNormalId(face)
    faceOffset = faceNormal * decalOffset
    extraOffset = faceNormal * decalDist # offset used to mitigate z-fighting
    localPosition = (faceOffset * size) + extraOffset
    match face:
        case Enum.NormalId.Right | Enum.NormalId.Left:
            # X
            size = size.zyx()
        case Enum.NormalId.Top | Enum.NormalId.Bottom:
            # Y
            size = size.xzy()
    localRotation = Matrix3.fromEulerAnglesYXZ(*faceRotations[face].yxz())
    localSpace = CoordinateFrame(localRotation, localPosition)
    rotation, position = getRotationAndPosition(worldTransform * localSpace)
    polyObject.Position = position
    polyObject.Rotation = rotation
    polyObject.Size = size

def HandleTexture(obj, polyObject):
    HandleDecal(obj, polyObject)
    studsPerTile = Vector2(obj.get('StudsPerTileU'), obj.get('StudsPerTileV'))
    offsetStuds = Vector2(obj.get('OffsetStudsU', 0), obj.get('OffsetStudsV', 0))
    size = polyObject.Size.xy()
    
    polyObject.TextureScale = studsPerTile / size
    polyObject.TextureOffset = offsetStuds / size
    

def HandleTruss(obj, polyObject):
    HandlePart(obj, polyObject)

def HandleMeshPart(obj, polyObject):
    polyObject.AssetId = int(getResource(obj.get('MeshId')))
    HandlePart(obj, polyObject)

def HandleUnionOperation(obj, polyObject):
    polyObject.AssetId = int(getResource(obj.get('AssetId')))
    HandlePart(obj, polyObject)

RANGE_CONV_CONSTANT = 5.25 # grabbed from RTP plugin
BRIGHTNESS_CONV_CONSTANT = 2.5 # grabbed from RTP plugin

def HandlePointLight(obj, polyObject):
    polyObject.Range = obj.get('Range')*RANGE_CONV_CONSTANT
    polyObject.Brightness = obj.get('Brightness')*BRIGHTNESS_CONV_CONSTANT
    polyObject.Color = Color4.FromColor3(obj.get('Color'))
    polyObject.Shadows = obj.get('Shadows')

def HandleSpotlight(obj, polyObject):
    # Spotlight doesn't inherit from PointLight
    # call HandlePointLight anyways due to Spotlight and PointLight having pretty much the same properties
    polyObject.Angle = obj.get('Angle')
    HandlePointLight(obj, polyObject)

def isSoundSource(obj, polyObject):
    return isinstance(polyObject, Part) or obj.className == "Attachment"

def HandleSound(obj, polyObject):
    polyObject.SoundID = getResource(obj.get('SoundId'))
    polyObject.Pitch = obj.get('PlaybackSpeed', obj.get('Pitch'))
    polyObject.Autoplay = obj.get('Playing', False)
    polyObject.Loop = obj.get('Looped')
    polyObject.PlayInWorld = isSoundSource(obj.parent, polyObject.parent)
    polyObject.Volume = obj.get('Volume')

def HandleAttachment(obj, polyObject):
    partCF = obj.parent.get('CFrame', CoordinateFrame.IDENTITY)
    
    rotation, position = getRotationAndPosition(partCF * obj.get('CFrame'))
    polyObject.Position = position
    polyObject.Rotation = rotation
    

def HandleWorkspace(obj, polyObject):
    polyObject.addChild(Camera())
    polyObject.FogEnabled = services['Lighting'].has('FogStart')
    polyObject.FogStartDistance = services['Lighting'].get('FogStart', 0)
    polyObject.FogEndDistance = services['Lighting'].get('FogEnd', 0)
    polyObject.FogColor = Color4.FromColor3(services['Lighting'].get('FogColor', Color3.WHITE))

def HandleScreenGui(obj, polyObject):
    polyObject.Visible = obj.get('Enabled', True)
def HandleFrame(obj, polyObject):
    polyObject.Color = getColor4(obj, 'Background')
    polyObject.BorderColor = Color4.FromColor3(obj.get('BorderColor3'))
    polyObject.BorderWidth = obj.get('BorderSizePixel')
    HandleUIField(obj, polyObject)

def fixUIPosition(position):
    # seems to work for WTTTOR and NDS, may not work for other places
    position.scale.y = 1-position.scale.y
    position.offset.y = -position.offset.y

def HandleUIField(obj, polyObject):
    position = obj.get('Position')
    size = obj.get('Size')
    fixUIPosition(position)
    polyObject.PositionOffset = position.offset
    polyObject.PositionRelative = position.scale
    polyObject.SizeOffset = size.offset
    polyObject.SizeRelative = size.scale
    polyObject.Visible = obj.get('Visible')
    polyObject.ClipDescendants = obj.get('ClipsDescendants', False)

def HandleImageLabel(obj, polyObject):
    opacity = alpha(obj.get('ImageTransparency', 0))
    color = obj.get('ImageColor3', Color3.WHITE)
    polyObject.Color = Color4.FromColor3(color, opacity)
    polyObject.ImageID = getResource(obj.get('Image'))
    polyObject.Clickable = obj.className == 'ImageButton'
    HandleUIField(obj, polyObject)

# font size enum to actual sizes
fontSizes = {
    Enum.FontSize.Size8:  8,
    Enum.FontSize.Size9:  9,
    Enum.FontSize.Size10: 10,
    Enum.FontSize.Size11: 11,
    Enum.FontSize.Size12: 12,
    Enum.FontSize.Size14: 14,
    Enum.FontSize.Size18: 18,
    Enum.FontSize.Size24: 24,
    Enum.FontSize.Size36: 36,
    Enum.FontSize.Size48: 48,
    Enum.FontSize.Size28: 28,
    Enum.FontSize.Size32: 32,
    Enum.FontSize.Size42: 42,
    Enum.FontSize.Size60: 60,
    Enum.FontSize.Size96: 96
}
textXAlignToPolytoria = {
    Enum.TextXAlignment.Left:   TextJustify.Left,
    Enum.TextXAlignment.Right:  TextJustify.Right,
    Enum.TextXAlignment.Center: TextJustify.Center,
}

textYAlignToPolytoria = {
    Enum.TextYAlignment.Top:    TextVerticalAlign.Top,
    Enum.TextYAlignment.Center: TextVerticalAlign.Middle,
    Enum.TextYAlignment.Bottom: TextVerticalAlign.Bottom,
}

def nobr(text):
    return f'<nobr>{text}</nobr>'
def bold(text):
    return f'<b>{text}</b>'
def italic(text):
    return f'<i>{text}</i>'
#
fontMap = {
    "rbxasset://fonts/families/SourceSansPro.json":    TextFontPreset.SourceSans,
    "rbxasset://fonts/families/PressStart2P.json":     TextFontPreset.PressStart2P,
    "rbxasset://fonts/families/Montserrat.json":       TextFontPreset.Montserrat,
    "rbxasset://fonts/families/RobotoMono.json":       TextFontPreset.RobotoMono,
    "rbxasset://fonts/families/Michroma.json":         TextFontPreset.Orbitron,
    "rbxasset://fonts/families/ComicNeueAngular.json": TextFontPreset.ComicSansMS
}

FONT_SCALE = 1.5 # found this in the polytoria types dump, seems to be correct
def HandleTextLabel(obj, polyObject):
    polyObject.Text = obj.get('Text')
    polyObject.TextColor = getColor4(obj, 'Text')
    polyObject.JustifyText = textXAlignToPolytoria[obj.get('TextXAlignment')]
    polyObject.VerticalAlign = textYAlignToPolytoria[obj.get('TextYAlignment')]
    fontSize = obj.get('TextSize', fontSizes.get(obj.get('FontSize')))
    fontSize /= FONT_SCALE
    polyObject.FontSize = fontSize
    polyObject.MaxFontSize = fontSize
    polyObject.AutoSize = obj.get('TextScaled', False)
    font = obj.get('FontFace', FontFace.FromEnum(obj.get('Font')))
    match font.weight:
        case Enum.FontWeight.Bold:
            polyObject.Text = bold(polyObject.Text)
    if font.style == "Italic":
        polyObject.Text = italic(polyObject.Text)
    fontPreset = fontMap.get(font.family.url, TextFontPreset.SourceSans)
    polyObject.Font = fontPreset
    if not obj.get('TextWrap'):
        polyObject.Text = nobr(polyObject.Text)
    polyObject.OutlineColor = getColor4(obj, 'TextStroke')
    HandleFrame(obj, polyObject)

def HandleTextButton(obj, polyObject):
    polyObject.Interactable = obj.get('Active')
    HandleTextLabel(obj, polyObject)

def HandleTextBox(obj, polyObject):
    polyObject.Placeholder = obj.get('PlaceholderText', '')
    polyObject.PlaceholderColor = Color4.FromColor3(obj.get('PlaceholderColor3', Color3.BLACK))
    polyObject.IsMultiline = obj.get('MultiLine')
    polyObject.IsReadOnly = not obj.get('TextEditable', True)
    HandleTextLabel(obj, polyObject)

def HandleTool(obj, polyObject):
    polyObject.Droppable = obj.get('CanBeDropped', True)

def HandleSky(obj, polyObject):
    polyObject.TopId = int(getResource(obj.get('SkyboxUp')))
    polyObject.BottomId = int(getResource(obj.get('SkyboxDn')))
    polyObject.LeftId = int(getResource(obj.get('SkyboxLf')))
    polyObject.RightId = int(getResource(obj.get('SkyboxRt')))
    polyObject.FrontId = int(getResource(obj.get('SkyboxFt')))
    polyObject.BackId = int(getResource(obj.get('SkyboxBk')))

SECONDS_IN_MINUTE = 60

SECONDS_IN_HOUR = SECONDS_IN_MINUTE * 60

def getgametime():
    timeofday = services['Lighting'].get('TimeOfDay')
    hms = timeofday.split(":")
    hours   = int(hms[0])
    minutes = int(hms[1])
    seconds = int(hms[2])
    
    return seconds + (minutes * SECONDS_IN_MINUTE) + (hours * SECONDS_IN_HOUR)

def getSunRotation():
    para = LightingParameters(getgametime(), True, services['Lighting'].get('GeographicLatitude'))    
    cf = CoordinateFrame.CreateEmpty()
    cf.lookAt(para.lightDirection, Vector3.unitY)
    
    return cf.rotation

defaultSunColor = Color3(255/255, 244/255, 214/255)

def DoSunLight(polyObject):
    polyObject.Brightness = services['Lighting'].get('Brightness')
    polyObject.Color = Color4.FromColor3(services['Lighting'].get('OutdoorAmbient', defaultSunColor))
    polyObject.Rotation = fixRotation(getSunRotation())
    return polyObject

def HandleLighting(obj, polyObject):
    polyObject.AmbientColor = Color4.FromColor3(obj.get('Ambient'))
    polyObject.addChild(DoSunLight(SunLight()))

# used for instances that have no unique properties/don't need properties set
def HandleBase(obj, polyObject):
    pass

constructors = {
    "Backpack":       Backpack,
    "BoolValue":      BoolValue,
    "ColorValue":     ColorValue,
    "Decal":          Decal,
    "Environment":    Environment,
    "Folder":         Folder,
    "GUI":            GUI,
    "ImageSky":       ImageSky,
    "IntValue":       IntValue,
    "Lighting":       Lighting,
    "LocalScript":    LocalScript,
    "MeshPart":       MeshPart,
    "Model":          Model,
    "ModuleScript":   ModuleScript,
    "NetworkEvent":   NetworkEvent,
    "NPC":            NPC,
    "NumberValue":    NumberValue,
    "Part":           Part,
    "PlayerGUI":      PlayerGUI,
    "PointLight":     PointLight,
    "ScriptInstance": ScriptInstance,
    "Seat":           Seat,
    "ServerHidden":   ServerHidden,
    "Sound":          Sound,
    "Spotlight":      Spotlight,
    "StringValue":    StringValue,
    "Tool":           Tool,
    "Truss":          Truss,
    "UIButton":       UIButton,
    "UIImage":        UIImage,
    "UILabel":        UILabel,
    "UITextInput":    UITextInput,
    "UIView":         UIView,
    "Vector3Value":   Vector3Value
}

classHandlers = {
    "Accessory":        HandleModel,
    "Attachment":       HandleAttachment,
    "Backpack":         HandleBase,
    "BoolValue":        HandleValue,
    "Color3Value":      HandleColorValue,
    "Configuration":    HandleBase,
    "CornerWedgePart":  HandlePart,
    "Decal":            HandleDecal,
    "Folder":           HandleBase,
    "Frame":            HandleFrame,
    "GuiMain":          HandleScreenGui,
    "ImageButton":      HandleImageLabel,
    "ImageLabel":       HandleImageLabel,
    "IntValue":         HandleValue,
    "Lighting":         HandleLighting,
    "LocalScript":      HandleScript,
    "MeshPart":         HandleMeshPart,
    "Model":            HandleModel,
    "ModuleScript":     HandleScript,
    "NumberValue":      HandleValue,
    "Part":             HandlePart,
    "PointLight":       HandlePointLight,
    "RemoteEvent":      HandleBase,
    "ScreenGui":        HandleScreenGui,
    "Script":           HandleScript,
    "Seat":             HandlePart,
    "ServerStorage":    HandleBase,
    "Sky":              HandleSky,
    "Sound":            HandleSound,
    "SpawnLocation":    HandlePart,
    "SpotLight":        HandleSpotlight,
    "StarterGui":       HandleBase,
    "StarterPack":      HandleBase,
    "StockSound":       HandleSound,
    "StringValue":      HandleValue,
    "TextBox":          HandleTextBox,
    "TextButton":       HandleTextButton,
    "TextLabel":        HandleTextLabel,
    "Texture":          HandleTexture,
    "Tool":             HandleTool,
    "TrussPart":        HandleTruss,
    "UnionOperation":   HandleUnionOperation,
    "Vector3Value":     HandleValue,
    "VehicleSeat":      HandlePart,
    "WedgePart":        HandlePart,
    "Workspace":        HandleWorkspace,
}
if args.npcs:
    classHandlers["NPC"] = HandleNPC

aliases = {
    "Accessory":       "Model",
    "Attachment":      "Model",
    "Backpack":        "Folder",
    "Color3Value":     "ColorValue",
    "Configuration":   "Folder",
    "CornerWedgePart": "Part",
    "Frame":           "UIView",
    "GuiMain":         "GUI",
    "ImageButton":     "UIImage",
    "ImageLabel":      "UIImage",
    "RemoteEvent":     "NetworkEvent",
    "ScreenGui":       "GUI",
    "Script":          "ScriptInstance",
    "ServerStorage":   "ServerHidden",
    "Sky":             "ImageSky",
    "SpawnLocation":   "Part",
    "SpotLight":       "Spotlight",
    "StarterGui":      "PlayerGUI",
    "StarterPack":     "Backpack",
    "StockSound":      "Sound",
    "TextBox":         "UITextInput",
    "TextButton":      "UIButton",
    "TextLabel":       "UILabel",
    "Texture":         "Decal",
    "TrussPart":       "Truss",
    "UnionOperation":  "MeshPart",
    "VehicleSeat":     "Seat",
    "WedgePart":       "Part",
    "Workspace":       "Environment"
}

classNames = {}
for className, handler in classHandlers.items():
    classNames[className] = aliases.get(className, className)

charItems = [
    "Shirt",
    "Pants",
    "Humanoid"
]

def ModelModifier(obj):
    if not args.npcs:
        return 'Model'
    if not isValidCharacter(obj):
        return 'Model'
    return 'NPC'

objectmodifiers = {
    "Model": ModelModifier,
    "Part": PartModifier,
    "Seat": PartModifier,
    "VehicleSeat": PartModifier,
    "WedgePart": PartModifier,
    "MeshPart": PartModifier,
    "CornerWedgePart": PartModifier,
    "TrussPart": PartModifier,
    "SpawnLocation": PartModifier,
    "UnionOperation": PartModifier
}

# this list acts sort of like a todo list
doNotConvert = [
    "Timer",
    "ObjectValue",                # Do later
    "Geometry",
    "Weld",
    "Snap",
    "Motor",
    "ManualWeld",
    "Glue",
    "Camera",
    "Hint",
    "Terrain",
    "WeldConstraint",
    "HingeConstraint",
    "RopeConstraint",
    "CylindricalConstraint",      # Do later
    "PrismaticConstraint",        # Do later
    "ParticleEmitter",            # Do later
    "SurfaceLight",               # Do later
    "Beam",                       # Do later
    "SelectionBox",               # Do later
    "VectorForce",                # Do later
    "BillboardGui",               # Do later
    "SurfaceGui",                 # Do later
    "Rotate",
    "PitchShiftSoundEffect",
    "ReverbSoundEffect",
    "BodyPosition",               # Do later
    "BodyVelocity",               # Do later
    "BodyGyro",                   # Do later
    "BodyAngularVelocity",        # Do later
    "VelocityMotor",
    "RotateP",
    "BodyThrust",
    "ClickDetector",              # Do later
    "HopperBin",                  # Do later
    "ViewportFrame",              # Do later
    "UIGridLayout",
    "Highlight",
    "Fire",                       # Do later
    "DialogChoice",
    "Dialog",
    "Smoke",                      # Do later
    "RemoteFunction",
    "Animation",                  # Do later
    "ScrollingFrame",             # Do later
    "SunRaysEffect",
    "ColorCorrectionEffect",
    "BloomEffect",
]

if not args.npcs:
    doNotConvert += charItems

doNotConvert += meshClasses


limbs = [
    "Head",
    "Torso",
    "Left Arm",
    "Right Arm",
    "Left Leg",
    "Right Leg"
]

def getConstructor(className):
    return constructors[classNames[className]]

def HandleObject(obj, parent=game):
    className = obj.className
    if className in doNotConvert:
        return
    polyObject = None
    if className in classHandlers:
        className = objectmodifiers.get(className, lambda x: x.className)(obj)
        handler = classHandlers[className]        
        polyObject = getConstructor(className)()
        polyObject.Name = polyObject.get('Name', obj.get('Name'))
        parent.addChild(polyObject)
        handler(obj, polyObject)
    else:
        print(f"UNSUPPORTED: {className}")
    if className == 'NPC':
        for child in obj.children:
            if child.className in charItems:
                continue
            if child.get('Name') in limbs:
                continue
            HandleObject(child, polyObject)
    else:
        for child in obj.children:
            HandleObject(child, polyObject)

def HandleService(service):
    if service in services:
        HandleObject(services[service])
    else:
        game.addChild(getConstructor(service)())

HandleService('Workspace')
HandleService('Lighting')
game.addChild(Players())
game.addChild(ScriptService())
game.addChild(Hidden())
HandleService('ServerStorage')
game.addChild(PlayerDefaults())
HandleService('StarterPack')
HandleService('StarterGui')

# lighting storage
hidden = game.findService('Hidden')

storageLighting = Folder()
storageLighting.Name = 'Storage from lighting'
hidden.addChild(storageLighting)

lighting = game.findService('Lighting')

lighting.moveChildren(storageLighting, ['ImageSky', 'SunLight'])

game.write(writer)

writer.close()