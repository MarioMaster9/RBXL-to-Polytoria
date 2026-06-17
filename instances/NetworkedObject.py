import uuid
from data_types import Color
from data_types import NumberRange
from data_types import NumberSeries
from data_types import Vector2
from data_types import Vector3

expectedTypes = {
    "array":           list,
    "boolean":         bool,
    "color":           Color,
#    "colorseries":     ColorSeries,
    "float":           float,
    "int":             int,
    "numberrange":     NumberRange,
    "numberseries":    NumberSeries,
    "ref":             object,
    "resourceref":     object,
    "string":          str,
    "uint":            int,
    "vector2":         Vector2,
    "vector3":         Vector3,
}

class NetworkedObject:
    ClassName = "NetworkedObject"
    Properties = {
        "Name": "string"
    }
    def __init__(self):
        self.children = []
        self.uuid = uuid.uuid4()
        self.addProperties(NetworkedObject.Properties)
    def setRandomName(self):
        self.Name = str(self.uuid)
    def __setattr__(self, name, value):
        if hasattr(self, "classProperties"):
            if name in self.classProperties:
                datatype = self.classProperties[name]
                if datatype != "ref" and datatype != "resourceref":
                    if not datatype in expectedTypes:
                        print(f"MISSING TYPE: {datatype}")
                        exit()
                    _type = expectedTypes[datatype]
                    assert type(value) is _type, f'type mismatch! expected {_type}, got {type(value)}'
        super().__setattr__(name, value)
    @property
    def className(self):
        return self.__class__.ClassName
    def addProperties(self, properties):
        if hasattr(self, "classProperties"):
            self.classProperties = properties | self.classProperties
        else:
            self.classProperties = properties
    def get(self, prop, default=None):
        if not hasattr(self, prop):
            return default
        return getattr(self, prop)
    def findFirstChildOfClass(self, classToFind):
        for child in self.children:
            if child.className == classToFind:
                return child
        return None
    def moveChildren(self, newParent, ignoreList):
        children = []
        for child in self.children:
            if child.className in ignoreList:
                continue
            children.append(child)
        
        for child in children:
            child.move(newParent)
    def addChild(self, obj):
        obj.parent = self
        self.children.append(obj)
    def move(self, newParent):
        self.parent.children.remove(self)
        newParent.addChild(self)
    def serialize(self, json_self):
        for propName, datatype in self.classProperties.items():
            if propName == "Name":
                continue
            if not hasattr(self, propName):
                continue
            prop = getattr(self, propName)
            if datatype == "ref" or datatype == "resourceref":
                # more lenient
                if prop is None:
                    print(f'{propName} of {self.className} is None')
            else:
                assert not prop is None, f'{propName} of {self.className} is None'
            match datatype:
                case "string" | "uint" | "int" | "float" | "boolean" | "array":
                    json_self["Properties"][propName] = prop
                case "ref" | "resourceref":
                    if prop is None:
                        json_self["Properties"][propName] = ""
                    else:
                        json_self["Properties"][propName] = str(prop.uuid)
                case "vector2" | "vector3" | "color" | "numberrange" | "numberseries" | "colorseries":
                    json_self["Properties"][propName] = prop.json()
                case _:
                    print("INVALID DATATYPE: " + datatype)
                    exit()
    def json(self):
        name = self.Name
        if self.parent is None:
            pass
        elif not (self.className == "World" or self.parent.className == "World"):
            name += str(self.uuid)
        json_self = {
            "Name": name,
            "ClassName": self.className,
            "ID": str(self.uuid),
            "Properties": {},
            "Children": [],
            "LinkedModel": None,
            "IsLinkedChild": False
        }

        self.serialize(json_self)
        for obj in self.children:
            json_self["Children"].append(obj.json())
        return json_self
    def resourcePass(self, root):
        # serialization pass that goes through all resource references
        for propName, datatype in self.classProperties.items():
            if datatype != "resourceref":
                continue
            if not hasattr(self, propName):
                continue
            prop = getattr(self, propName)
            if prop is None:
                continue
            if not prop.included:
                prop.included = True
                root.nonInstanceObjects.append(prop)
        for obj in self.children:
            obj.resourcePass(root)