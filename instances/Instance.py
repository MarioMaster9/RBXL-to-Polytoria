class Instance:
    ClassName = "Instance"
    Properties = [
        ["Name", "string"]
    ]
    def __init__(self):
        self.children = []
        self.addProperties(Instance.Properties)
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
    def addChild(self, obj):
        obj.parent = self
        self.children.append(obj)
    def move(self, newParent):
        self.parent.children.remove(self)
        newParent.addChild(self)
    def serializeNew(self, writer):
        for item in self.serializationProperties:
            propName = item[0]
            datatype = item[1]
            if not hasattr(self, item[0]):
                continue
            assert not getattr(self, item[0]) is None, f'{item[0]} of {self.className} is None'
            match item[1]:
                case "boolean":
                    writer.writeBoolean(item[0], getattr(self, item[0]))
                case "string":
                    writer.writeString(item[0], getattr(self, item[0]))
                case "int":
                    writer.writeInt(item[0], getattr(self, item[0]))
                case "float":
                    writer.writeFloat(item[0], getattr(self, item[0]))
                case "color":
                    writer.writeColor(item[0], getattr(self, item[0]))
                case "vector2":
                    writer.writeVector2(item[0], getattr(self, item[0]))
                case "vector3":
                    writer.writeVector3(item[0], getattr(self, item[0]))
                case "numberrange":
                    writer.writeNumberRange(item[0], getattr(self, item[0]))
                case "colorrange":
                    writer.writeColorRange(item[0], getattr(self, item[0]))
                case _:
                    print("INVALID DATATYPE: " + datatype)
                    exit()
    def write(self, writer):
        writer.writeDataOpening(f'<Item class="{self.className}">')
        writer.writeDataOpening(f'<Properties>')
        self.serializeNew(writer)
        writer.writeDataClosing("</Properties>")
        for obj in self.children:
            obj.write(writer)
        writer.writeDataClosing("</Item>")