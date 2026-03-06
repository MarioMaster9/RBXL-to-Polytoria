import base64
from data_types.Color3                 import Color3
from data_types.Content                import Content
from data_types.ColorSequence          import ColorSequence
from data_types.CoordinateFrame        import CoordinateFrame
from data_types.FontFace               import FontFace
from data_types.NumberRange            import NumberRange
from data_types.NumberSequence         import NumberSequence
from data_types.PhysicalProperties     import PhysicalProperties
from data_types.UDim2                  import UDim2
from data_types.Vector2                import Vector2
from data_types.Vector3                import Vector3

class TreeItem:
    def __init__(self, elem, parent):
        self.custom = {}
        self.children = []
        if not parent is None:
            self.className = elem.attrib['class']
            if self.className == "Model":
                self.setcustom('hasHumanoid', False)
            self.properties = InstanceTree.GetProperties(elem)
            self.parent = parent
            if self.className == "Humanoid":
                self.parent.setcustom('hasHumanoid', True)
    def get(self, prop, default=None):
        return self.properties.get(prop, default)
    def set(self, prop, value):
        self.properties[prop] = value
    def has(self, prop):
        return prop in self.properties
    def getcustom(self, prop, default=None):
        return self.custom.get(prop, default)
    def setcustom(self, prop, value):
        self.custom[prop] = value
    def findFirstChildOfClass(self, className):
        for child in self.children:
            if child.className == className:
                return child
        return None
    def findFirstChild(self, name):
        for child in self.children:
            if child.get('Name') == name:
                return child
        return None

# text attribute returns None if there is no data, so return an empty string if it is None
# Fixes a few issues
getText = lambda x: x.text or ''

# just return the element, used if the type is not fully implemented but may be required in the future
basicDeserialize = lambda x: x

def basicDeserialize_Report(x):
    print(x.tag)
    return x

booleanDeserialize = lambda x: x.text=="true"
floatDeserialize = lambda x: float(x.text)
intDeserialize = lambda x: int(x.text)
base64Deserialize = lambda x: base64.b64decode(getText(x))

# Deserializers
xmlHandlers = {
    "BinaryString":       base64Deserialize,
    "bool":               booleanDeserialize,
    "ColorSequence":      ColorSequence.FromXML,
    "Color3":             Color3.FromXML,
    "Color3uint8":        Color3.FromXML,
    "Content":            Content.FromXML,
    "CoordinateFrame":    CoordinateFrame.FromXML,
    "double":             floatDeserialize,
    "float":              floatDeserialize,
    "Font":               FontFace.FromXML,
    "int":                intDeserialize,
    "int64":              intDeserialize,
    "NumberRange":        NumberRange.FromXML,
    "NumberSequence":     NumberSequence.FromXML,
    "PhysicalProperties": PhysicalProperties.FromXML,
    "ProtectedString":    getText,
    "Ref":                basicDeserialize,
    "string":             getText,
    "token":              intDeserialize,
    "UDim2":              UDim2.FromXML,
    "Vector2":            Vector2.FromXML,
    "Vector3":            Vector3.FromXML
}


skippedTags = [
    "OptionalCoordinateFrame",
    "SecurityCapabilities",
    "SharedString",
    "UniqueId",
    "NetAssetRef"
]

class InstanceTree:
    @staticmethod
    def GetProperties(obj):
        propertyElem = obj.find("Properties")
        properties = {}
        for elem in propertyElem:
            if elem.tag in skippedTags:
                continue
            handler = xmlHandlers.get(elem.tag, basicDeserialize_Report)
            properties[elem.attrib['name']] = handler(elem)
        return properties
    @staticmethod
    def CreateRoot(elem):
        return TreeItem(elem, None)
    @staticmethod
    def BuildTree(elem, obj):
        for child in elem:
            if child.tag != 'Item':
                continue
            newItem = TreeItem(child, obj)
            obj.children.append(newItem)
            InstanceTree.BuildTree(child, newItem)