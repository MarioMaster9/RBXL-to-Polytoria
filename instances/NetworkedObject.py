import uuid

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
                case "color":
                    r = int(prop.r*255)
                    g = int(prop.g*255)
                    b = int(prop.b*255)
                    a = int(prop.a*255)
                    json_self["Properties"][propName] = f'{r:02x}{g:02x}{b:02x}{a:02x}'
                case "vector2" | "vector3":
                    json_self["Properties"][propName] = [*prop]
                case "numberrange":
                    #TODO: implement
                    json_self["Properties"][propName] = ""#prop
                case "colorrange":
                    #TODO: implement
                    json_self["Properties"][propName] = ""#prop
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
        for item in self.serializationProperties:
            propName = item[0]
            datatype = item[1]
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