USE_WELDS = False

import json
from multimethod import multimethod
from json.decoder import JSONDecodeError
from datetime import datetime, timezone
import rbxl

import shutil
import math
import util.hashfuncs as hashfuncs
import argparse
import os

#from rbxl.data_types import *
from data_types import *
from enums import *
from instances import *

from rbxl.data_types import Matrix3
from rbxl.data_types import Enum
from rbxl.data_types import Content
from rbxl.data_types import MeshInfo
from rbxl.data_types import CoordinateFrame
from rbxl.data_types import BrickColor
from rbxl.data_types import Color3

import util.extmath as extmath

from util.EnumMigrator           import EnumMigrator
from util.LightingParameters     import LightingParameters
from util.JSONWriter             import JSONWriter
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
                    description='Converts RBXL files to Polytoria')
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

game = Game("2.0.0-beta85")
world = World()
game.addChild(world)

services = {}

rbxlFile = rbxl.parse(args.filename)
for child in rbxlFile.root.children:
    services[child.className] = child
writer = JSONWriter(f'out/{args.outfile}.poly')

# convert transparency to opacity
def alpha(transparency):
    return 1-min(1, transparency)

def getBrickColor3(brickColorValue):
    return BrickColor.ColorMap[brickColorValue]

def getPartColor3(obj):
    return obj.get('Color3uint8', getBrickColor3(obj.get('BrickColor')))

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
    return Color(*obj.get(propType + "Color3", Color3.BLACK), alpha(obj.get(propType + "Transparency", 1)))

@multimethod
def getColor4(obj: TreeItem, color3: str, transparency: str):
    # color4 method, separating property names. safer, but it may look messier
    return Color(*obj.get(color3), alpha(obj.get(transparency)))

def getPartColor4(obj):
    # color4 method for parts, due to part color property name and datatype changes in various versions
    return Color(*getPartColor3(obj), alpha(obj.get('Transparency')))

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
    return ""#scriptSources[config_scriptNames.get(scriptHash)]

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
    return euler

def getRotationAndPosition(cf):
    return fixRotation(cf.rotation), cf.translation

baseParts = [
    "CornerWedgePart",
    "Part",
    "FlagStand",
    "Seat",
    "SkateboardPlatform",
    "SpawnLocation",
    "WedgePart",
    "Terrain",
    "MeshPart",
    "PartOperation",
    "IntersectOperation",
    "NegateOperation",
    "UnionOperation",
    "TrussPart",
    "VehicleSeat"
]

def HandleModel(obj, polyObject):
    descendants = obj.getdescendants()
    position = Vector3(0, 0, 0)
    partCount = 0
    for descendant in descendants:
        if not descendant.className in baseParts:
            continue
        position += descendant.get("CFrame").translation
        partCount += 1
    if partCount != 0:
        position /= partCount
    polyObject.Position = position

def HandleNPC(obj, polyObject):
    shirt = obj.findFirstChildOfClass("Shirt")
    if not shirt is None:
        shirtInstance = Clothing()
        shirtInstance.Name = shirt.get('Name')
        shirtInstance.Image = ResourceFactory.CreateImage(getResource(shirt.get('ShirtTemplate')))
        polyObject.Character.addChild(shirtInstance)
    pants = obj.findFirstChildOfClass("Pants")
    if not pants is None:
        pantsInstance = Clothing()
        pantsInstance.Name = pants.get('Name')
        pantsInstance.Image = ResourceFactory.CreateImage(getResource(pants.get('PantsTemplate')))
        polyObject.Character.addChild(pantsInstance)
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
    character = polyObject.Character
    if not bodyColors is None:
        character.HeadColor.setColor3(bodyColors.get('HeadColor'))
        character.TorsoColor.setColor3(bodyColors.get('TorsoColor'))
        character.LeftArmColor.setColor3(bodyColors.get('LeftArmColor'))
        character.RightArmColor.setColor3(bodyColors.get('RightArmColor'))
        character.LeftLegColor.setColor3(bodyColors.get('LeftLegColor'))
        character.RightLegColor.setColor3(bodyColors.get('RightLegColor'))
    
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
    polyObject.Value = Color(*obj.get('Value'))

def HandleObjectValue(obj, polyObject):
    polyObject.Value = rbxlFile.getRef(obj.get('Value'))


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
    "1033714": {"shape": ShapeEnum.Cone, "scale": Vector3(2, 0.75, 2)}
}

typeShapes = {
    "UpCylinder": ShapeEnum.Cylinder,
    "Cylinder": ShapeEnum.Cylinder,
    "Block": ShapeEnum.Brick,
    "SphereMesh": ShapeEnum.Sphere,
    "Ball": ShapeEnum.Sphere,
    "Wedge": ShapeEnum.Wedge,
    "CornerWedge": ShapeEnum.Corner,
    "FileMesh": ShapeEnum.Brick
}

def getExtraPartInfo(obj):
    meshInfo = obj.getcustom('meshInfo')
    if meshInfo.type == 'FileMesh':
        if meshInfo.id.identifier in meshIdMap:
            info = meshIdMap[meshInfo.id.identifier]
            return info['shape'], info['scale']
    elif meshInfo.type == 'Truss':
        trussStyle = obj.get('style')
        return EnumMigrator.ToPolytoria(Enum.Style, trussStyle), Vector3.ONE
    return typeShapes.get(meshInfo.type, ShapeEnum.Brick), Vector3.ONE

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
        partColor = Color(*vertexColor, partColor.a)
    polyObject.Color = partColor
    
    # commented out due to objects not being welded together
    #polyObject.Anchored = obj.get('Anchored')
    polyObject.CanCollide = obj.get('CanCollide')
    polyObject.IsSpawn = obj.className == 'SpawnLocation'
    if polyObject.className != 'MeshPart':
        # MeshPart class doesn't have Shape property afaik
        polyObject.Shape = shape
    
    polyObject.Material = EnumMigrator.ToPolytoria(Enum.Material, obj.get('Material'), PartMaterialEnum.Plastic)
    polyObject.Velocity = obj.get('Velocity')
    polyObject.Friction = getPartFriction(obj)
    polyObject.Bounciness = getPartElasticity(obj)
        
    polyObject.Position = position
    polyObject.Rotation = rotation
    polyObject.Size = size

def HandleScript(obj, polyObject):
    if obj.get('Enabled') is None:
        polyObject.IsEnabled = not obj.get('Disabled', False)
    else:
        polyObject.IsEnabled = obj.get('Enabled')
    source = obj.get('Source')
    sourceHash = hashfuncs.md5(source)
    saveScript(source, sourceHash)
    polyObject.Source = getScriptSource(sourceHash)

def HandleParticleEmitter(obj, polyObject):
    #Acceleration
    #Brightness
    #Color
    #Drag
    #EmissionDirection
    polyObject.Playing = obj.get('Enabled')
    #FlipbookBlendFrames
    #FlipbookFramerate
    #FlipbookIncompatible
    #FlipbookLayout
    #FlipbookMode
    #FlipbookSizeX
    #FlipbookSizeY
    #FlipbookStartRandom
    lifetime = obj.get('Lifetime')
    polyObject.Lifetime = PTNumberRange(lifetime.min, lifetime.max)
    #LightEmission
    #LightInfluence
    polyObject.SimulationSpace = int(obj.get('LockedToPart'))
    #ParticleOrientation
    polyObject.Amount = obj.get('Rate')
    rotation = obj.get('Rotation')
    polyObject.StartRotation = PTNumberRange(rotation.min, rotation.max)
    rotSpeed = obj.get('RotSpeed')
    polyObject.AngularVelocity = PTNumberRange(rotSpeed.min, rotSpeed.max)
    #Shape
    #ShapeInOut
    #ShapePartial
    #ShapeStyle
    #Size
    speed = obj.get('Speed')
    polyObject.InitialVelocity = PTNumberRange(speed.min, speed.max)
    #SpreadAngle
    #Squash
    polyObject.Image = ResourceFactory.CreateImage(getResource(obj.get('Texture')))
    polyObject.SpeedScale = obj.get('TimeScale')
    #Transparency
    #VelocityInheritance
    #WindAffectsDrag
    #ZOffset




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

def HandleFaceObject(obj, polyObject):
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

def HandleDecal(obj, polyObject):
    if str(obj.get('Texture')) == '':
        polyObject.Color = Color(0, 0, 0, 0)
    polyObject.Image = ResourceFactory.CreateImage(getResource(obj.get('Texture')))
    HandleFaceObject(obj, polyObject)


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
    polyObject.Asset = ResourceFactory.CreateMesh(getResource(obj.get('MeshId')))
    HandlePart(obj, polyObject)

def HandleUnionOperation(obj, polyObject):
    polyObject.Asset = ResourceFactory.CreateMesh(getResource(obj.get('AssetId')))
    polyObject.UsePartColor = obj.get('UsePartColor')
    HandlePart(obj, polyObject)

RANGE_CONV_CONSTANT = 5.25 # grabbed from RTP plugin
BRIGHTNESS_CONV_CONSTANT = 2.5 # grabbed from RTP plugin

def HandlePointLight(obj, polyObject):
    polyObject.Range = obj.get('Range')*RANGE_CONV_CONSTANT
    polyObject.Brightness = obj.get('Brightness')*BRIGHTNESS_CONV_CONSTANT
    polyObject.Color = Color(*obj.get('Color'))
    polyObject.Shadows = obj.get('Shadows')

def HandleSpotLight(obj, polyObject):
    # SpotLight doesn't inherit from PointLight
    # call HandlePointLight anyways due to SpotLight and PointLight having pretty much the same properties
    polyObject.Angle = obj.get('Angle')
    HandlePointLight(obj, polyObject)

def isSoundSource(obj, polyObject):
    return isinstance(polyObject, Part) or obj.className == "Attachment"

def HandleSound(obj, polyObject):
    polyObject.Audio = ResourceFactory.CreateAudio(getResource(obj.get('SoundId')))
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

def HandleTeam(obj, polyObject):
    polyObject.Color = Color(*getBrickColor3(obj.get('TeamColor')))

def HandleWeld(obj, polyObject):
    polyObject.Part0 = rbxlFile.getRef(obj.get('Part0'))
    polyObject.Part1 = rbxlFile.getRef(obj.get('Part1'))
    polyObject.Enabled = False#obj.get('Enabled', True)

def HandleBodyPosition(obj, polyObject):
    polyObject.Force = obj.get('p', obj.get('P'))
    polyObject.TargetPosition = obj.get('position', obj.get('Position'))

def HandleWorkspace(obj, polyObject):
    polyObject.addChild(Camera())

def HandleScreenGui(obj, polyObject):
    polyObject.Visible = obj.get('Enabled', True)
def HandleFrame(obj, polyObject):
    polyObject.Color = getColor4(obj, 'Background')
    polyObject.BorderColor = Color(*obj.get('BorderColor3'))
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
    polyObject.IgnoreMouse = not obj.get('Active', False)
    polyObject.ZIndex = obj.get('ZIndex')

def HandleImageLabel(obj, polyObject):
    opacity = alpha(obj.get('ImageTransparency', 0))
    color = obj.get('ImageColor3', Color3.WHITE)
    polyObject.Color = Color(*color, opacity)
    polyObject.Image = ResourceFactory.CreateImage(getResource(obj.get('Image')))
    polyObject.Clickable = obj.className == 'ImageButton'
    polyObject.TextureScale = Vector2.ONE#obj.get('ImageRectSize', Vector2.ONE)
    polyObject.TextureOffset = Vector2.ZERO#obj.get('ImageRectOffset', Vector2.ZERO)
    polyObject.TextureFilter = EnumMigrator.ToPolytoria(Enum.ResamplerMode, obj.get('ResampleMode', 0))
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

#
fontMap = {
    "rbxasset://fonts/families/SourceSansPro.json":    BuiltInTextFontPresetEnum.SourceSans,
    "rbxasset://fonts/families/PressStart2P.json":     BuiltInTextFontPresetEnum.PressStart2P,
    "rbxasset://fonts/families/Montserrat.json":       BuiltInTextFontPresetEnum.Montserrat,
    "rbxasset://fonts/families/RobotoMono.json":       BuiltInTextFontPresetEnum.RobotoMono,
    "rbxasset://fonts/families/Michroma.json":         BuiltInTextFontPresetEnum.Orbitron,
    "rbxasset://fonts/families/ComicNeueAngular.json": BuiltInTextFontPresetEnum.ComicSansMS
}

FONT_SCALE = 1.5 # found this in the polytoria types dump, seems to be correct
def HandleTextLabel(obj, polyObject):
    polyObject.Text = obj.get('Text')
    polyObject.TextColor = getColor4(obj, 'Text')
    polyObject.HorizontalAlignment = EnumMigrator.ToPolytoria(Enum.TextXAlignment, obj.get('TextXAlignment'))
    polyObject.VerticalAlignment = EnumMigrator.ToPolytoria(Enum.TextYAlignment, obj.get('TextYAlignment'))
    fontSize = obj.get('TextSize', fontSizes.get(obj.get('FontSize')))
    fontSize /= FONT_SCALE
    polyObject.FontSize = fontSize
    polyObject.MaxAutoSize = fontSize
    polyObject.AutoSize = obj.get('TextScaled', False)
    font = obj.get('FontFace', FontFace.FromEnum(obj.get('Font')))
    fontPreset = fontMap.get(font.family.url, BuiltInTextFontPresetEnum.SourceSans)
    fontWeight = EnumMigrator.ToPolytoria(Enum.FontWeight, font.weight)
    fontStyle = int(font.style == "Italic")

    fontAsset = ResourceFactory.CreateFont(fontPreset, fontWeight, fontStyle)
    polyObject.FontAsset = fontAsset
    polyObject.TextWrapped = obj.get('TextWrap', obj.get('TextWrapped'))
    polyObject.OutlineColor = getColor4(obj, 'TextStroke')
    HandleFrame(obj, polyObject)

def HandleTextButton(obj, polyObject):
    #polyObject.Interactable = obj.get('Active')
    HandleTextLabel(obj, polyObject)

def HandleTextBox(obj, polyObject):
    polyObject.Placeholder = obj.get('PlaceholderText', '')
    polyObject.PlaceholderColor = Color(*obj.get('PlaceholderColor3', Color3.BLACK))
    polyObject.MultiLine = obj.get('MultiLine')
    polyObject.ReadOnly = not obj.get('TextEditable', True)
    HandleTextLabel(obj, polyObject)

def HandleTool(obj, polyObject):
    polyObject.Droppable = obj.get('CanBeDropped', True)
    polyObject.IconImage = ResourceFactory.CreateImage(getResource(obj.get('TextureId')))

def HandleSky(obj, polyObject):
    polyObject.TopImage = ResourceFactory.CreateImage(getResource(obj.get('SkyboxUp')))
    polyObject.BottomImage = ResourceFactory.CreateImage(getResource(obj.get('SkyboxDn')))
    polyObject.LeftImage = ResourceFactory.CreateImage(getResource(obj.get('SkyboxLf')))
    polyObject.RightImage = ResourceFactory.CreateImage(getResource(obj.get('SkyboxRt')))
    polyObject.FrontImage = ResourceFactory.CreateImage(getResource(obj.get('SkyboxFt')))
    polyObject.BackImage = ResourceFactory.CreateImage(getResource(obj.get('SkyboxBk')))

def getgametime():
    timeofday = services['Lighting'].get('TimeOfDay')
    timestamp = datetime.strptime(timeofday, '%H:%M:%S').replace(tzinfo=timezone.utc)
    return int(timestamp.timestamp())

def getSunRotation():
    para = LightingParameters(getgametime(), True, services['Lighting'].get('GeographicLatitude'))    
    cf = CoordinateFrame.CreateEmpty()
    cf.lookAt(para.lightDirection, Vector3.unitY)
    
    return cf.rotation

defaultSunColor = Color3(255/255, 244/255, 214/255)

def DoSunLight(polyObject):
    polyObject.Brightness = services['Lighting'].get('Brightness')
    polyObject.Color = Color(*services['Lighting'].get('OutdoorAmbient', defaultSunColor))
    polyObject.Rotation = fixRotation(getSunRotation())
    return polyObject

def HandleLighting(obj, polyObject):
    polyObject.AmbientColor = Color(*obj.get('Ambient'))
    polyObject.FogEnabled = services['Lighting'].has('FogStart')
    polyObject.FogStartDistance = services['Lighting'].get('FogStart', 0)
    polyObject.FogEndDistance = services['Lighting'].get('FogEnd', 0)
    polyObject.FogColor = Color(*services['Lighting'].get('FogColor', Color3.WHITE))
    polyObject.addChild(DoSunLight(SunLight()))


# used for instances that have no unique properties/don't need properties set
def HandleBase(obj, polyObject):
    pass

classHandlers = {
    "Accessory":        HandleModel,
    "Attachment":       HandleAttachment,
    "Backpack":         HandleBase,
    "BodyPosition":     HandleBodyPosition,
    "BoolValue":        HandleValue,
    "Color3Value":      HandleColorValue,
    "Configuration":    HandleBase,
    "CornerWedgePart":  HandlePart,
    "Decal":            HandleDecal,
    "Folder":           HandleBase,
    "Frame":            HandleFrame,
    "Glue":             HandleWeld,
    "GuiMain":          HandleScreenGui,
    "ImageButton":      HandleImageLabel,
    "ImageLabel":       HandleImageLabel,
    "IntValue":         HandleValue,
    "Lighting":         HandleLighting,
    "LocalScript":      HandleScript,
    "ManualWeld":       HandleWeld,
    "MeshPart":         HandleMeshPart,
    "Model":            HandleModel,
    "ModuleScript":     HandleScript,
    "ObjectValue":      HandleObjectValue,
    "NumberValue":      HandleValue,
    "Part":             HandlePart,
    "PointLight":       HandlePointLight,
    "RemoteEvent":      HandleBase,
    "ScreenGui":        HandleScreenGui,
    "Script":           HandleScript,
    "Seat":             HandlePart,
    "ServerStorage":    HandleBase,
    "Sky":              HandleSky,
    "Snap":             HandleWeld,
    "Sound":            HandleSound,
    "SpawnLocation":    HandlePart,
    "SpotLight":        HandleSpotLight,
    "StarterGui":       HandleBase,
    "StarterPack":      HandleBase,
    "StockSound":       HandleSound,
    "StringValue":      HandleValue,
    "Team":             HandleTeam,
    "Teams":            HandleBase,
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
    "Weld":             HandleWeld,
    "Workspace":        HandleWorkspace,
}
if args.npcs:
    classHandlers["NPC"] = HandleNPC

with open('converter_configuration/aliases.json', 'r') as f:
    aliases = json.load(f)

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
    "Geometry",
    "Motor",
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

if not USE_WELDS:
    doNotConvert += ["Weld", "Glue", "ManualWeld", "Snap"]

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

def HandleObject(obj, parent=world):
    className = obj.className
    if className in doNotConvert:
        return
    polyObject = None
    if className in classHandlers:
        className = objectmodifiers.get(className, lambda x: x.className)(obj)
        handler = classHandlers[className]        
        polyObject = Instance.New(classNames[className])
        polyObject.Name = polyObject.get('Name', obj.get('Name'))
        obj.gameObject = polyObject
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

def ReferencesPass(obj):
    if hasattr(obj, "serializationProperties"):
        for item in obj.serializationProperties:
            propName = item[0]
            datatype = item[1]
            if propName != "ref":
                continue
            if not hasattr(obj, propName):
                continue
            prop = getattr(obj, propName)
            if prop is None:
                continue
            if not isinstance(prop, TreeItem):
                continue
            setattr(obj, propName, prop.gameObject)
    for obj2 in obj.children:
        ReferencesPass(obj2)



def HandleService(service, parent=world):
    if service in services:
        HandleObject(services[service], parent)
    else:
        parent.addChild(Instance.New(classNames[service]))

HandleService('Workspace')
HandleService('Lighting')
world.addChild(Players())
world.addChild(ScriptService())
world.addChild(Hidden())
HandleService('ServerStorage')
playerDefaults = PlayerDefaults()
world.addChild(playerDefaults)
HandleService('StarterPack', playerDefaults)
HandleService('StarterGui')
world.addChild(AchievementsService())
world.addChild(CoreUIService())
world.addChild(Stats())
HandleService('Teams')
world.addChild(CaptureService())

# lighting storage
hidden = world.findService('Hidden')

storageLighting = Folder()
storageLighting.Name = 'Storage from lighting'
hidden.addChild(storageLighting)

lighting = world.findService('Lighting')

lighting.moveChildren(storageLighting, ['ImageSky', 'SunLight'])

ReferencesPass(game)
game_json = game.json()

writer.write(game_json)
projectWriter = JSONWriter("out/project.ptproj")
projectWriter.write({
    "ProjectName": "MyProject",
    "MainWorld": args.outfile + '2.poly', # temporary
    "IconID": None
})


writer.close()
projectWriter.close()