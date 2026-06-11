import uuid
from rbxl.util.InstanceTree import TreeItem

class NetworkedObject:
    ClassName = "NetworkedObject"
    Properties = [
        ["Name", "string"]
    ]
    def __init__(self):
        self.children = []
        self.uuid = uuid.uuid4()
        self.addProperties(NetworkedObject.Properties)
    def setRandomName(self):
        self.Name = str(self.uuid)
    @property
    def className(self):
        return self.__class__.ClassName
    def addProperties(self, properties):
        if hasattr(self, "serializationProperties"):
            self.serializationProperties = properties + self.serializationProperties
        else:
            self.serializationProperties = properties
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
        for item in self.serializationProperties:
            propName = item[0]
            datatype = item[1]
            if propName == "Name":
                continue
            if not hasattr(self, item[0]):
                continue
            if item[1] == "ref":
                # more lenient
                if getattr(self, item[0]) is None:
                    print(f'{item[0]} of {self.className} is None')
            else:
                assert not getattr(self, item[0]) is None, f'{item[0]} of {self.className} is None'
            match item[1]:
                case "string" | "uint" | "int" | "float" | "boolean" | "array":
                    json_self["Properties"][item[0]] = getattr(self, item[0])
                case "ref":
                    prop = getattr(self, item[0])
                    if isinstance(prop, TreeItem):
                        if not prop.gameObject is None:
                            json_self["Properties"][item[0]] = str(prop.gameObject.uuid)
                    elif not prop is None:
                        json_self["Properties"][item[0]] = str(getattr(self, item[0]).uuid)
                case "color":
                    value = getattr(self, item[0])
                    r = int(value.r*255)
                    g = int(value.g*255)
                    b = int(value.b*255)
                    a = int(value.a*255)
                    json_self["Properties"][item[0]] = f'{r:02x}{g:02x}{b:02x}{a:02x}'
                case "vector2" | "vector3":
                    json_self["Properties"][item[0]] = [*getattr(self, item[0])]
                case "numberrange":
                    #TODO: implement
                    json_self["Properties"][item[0]] = ""#getattr(self, item[0])
                case "colorrange":
                    #TODO: implement
                    json_self["Properties"][item[0]] = ""#getattr(self, item[0])
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